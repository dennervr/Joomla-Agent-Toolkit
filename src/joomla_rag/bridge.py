import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any


class AgentBridge:
    """Bridge for executing PHP code and commands within Joomla context."""

    def __init__(self, joomla_path: Path):
        self.joomla_path = joomla_path
        self.php_script_path = joomla_path / "cli" / "agent_cli.php"

    def deploy_php_script(self):
        """Deploy the PHP CLI script to Joomla's cli directory."""
        cli_dir = self.joomla_path / "cli"
        cli_dir.mkdir(exist_ok=True)
        
        php_content = self._get_php_script_content()
        self.php_script_path.write_text(php_content)

    def run_command(self, command: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Run a command via the PHP script."""
        if not self.php_script_path.exists():
            raise FileNotFoundError(f"PHP script not found at {self.php_script_path}. Run deploy_php_script() first.")
        
        # Prepare JSON payload
        json_payload = json.dumps({"command": command, **payload})
        
        # Run PHP script with JSON payload via stdin
        result = subprocess.run(
            ["php", str(self.php_script_path), f"agent:{command}"],
            input=json_payload,
            text=True,
            capture_output=True,
            cwd=self.joomla_path
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"PHP script failed: {result.stderr}")
        
        try:
            return json.loads(result.stdout.strip())
        except json.JSONDecodeError:
            raise RuntimeError(f"Invalid JSON output from PHP script: {result.stdout}")

    def run_php_code(self, code: str) -> Dict[str, Any]:
        """Execute arbitrary PHP code within Joomla context."""
        return self.run_command("run", {"code": code})

    def trace_route(self, route: str) -> Dict[str, Any]:
        """Trace a Joomla route to find Itemid and menu details."""
        return self.run_command("trace", {"route": route})

    def get_api_token(self) -> Dict[str, Any]:
        """Generate or retrieve a Super User API token."""
        return self.run_command("auth", {})

    def _get_php_script_content(self) -> str:
        """Get the PHP script content."""
        php_lines = [
            '<?php',
            '/**',
            ' * Joomla Agent CLI Bridge',
            ' * ',
            ' * This script provides a bridge for executing PHP code and commands within Joomla context.',
            ' * It bootstraps Joomla properly and handles agent commands.',
            ' */',
            '',
            'define(\'_JEXEC\', 1);',
            'define(\'JPATH_BASE\', dirname(__DIR__));',
            '',
            '// Bootstrap Joomla',
            'require_once JPATH_BASE . \'/includes/defines.php\';',
            'require_once JPATH_BASE . \'/includes/framework.php\';',
            '',
            '// Boot the DI container',
            '$container = \\Joomla\\CMS\\Factory::getContainer();',
            '$container->alias(\\Joomla\\Session\\SessionInterface::class, \'session.web.site\');',
            '$app = $container->get(\\Joomla\\CMS\\Application\\SiteApplication::class);',
            '\\Joomla\\CMS\\Factory::$application = $app;',
            '',
            '// Read JSON payload from stdin',
            '$payload = json_decode(file_get_contents(\'php://stdin\'), true);',
            '',
            'if (json_last_error() !== JSON_ERROR_NONE) {',
            '    echo json_encode([\'error\' => \'Invalid JSON input\']);',
            '    exit(1);',
            '}',
            '',
            '$command = $payload[\'command\'] ?? \'\';',
            '$result = [];',
            '',
            '// Log the execution',
            '$log_entry = date(\'Y-m-d H:i:s\') . " - Command: {$command} - Payload: " . json_encode($payload) . "\\n";',
            'file_put_contents(JPATH_BASE . \'/logs/agent_audit.log\', $log_entry, FILE_APPEND);',
            '',
            'try {',
            '    switch ($command) {',
            '        case \'run\':',
            '            $result = execute_php_code($payload[\'code\'] ?? \'\');',
            '            break;',
            '        case \'trace\':',
            '            $result = trace_route($payload[\'route\'] ?? \'\');',
            '            break;',
            '        case \'auth\':',
            '            $result = get_api_token();',
            '            break;',
            '        default:',
            '            throw new Exception("Unknown command: {$command}");',
            '    }',
            '} catch (Exception $e) {',
            '    $result = [\'error\' => $e->getMessage()];',
            '}',
            '',
            '// Log the result',
            '$log_entry = date(\'Y-m-d H:i:s\') . " - Result: " . json_encode($result) . "\\n";',
            'file_put_contents(JPATH_BASE . \'/logs/agent_audit.log\', $log_entry, FILE_APPEND);',
            '',
            'echo json_encode($result);',
            '',
            'function execute_php_code($code) {',
            '    // Execute PHP code in Joomla context',
            '    ob_start();',
            '    eval($code);',
            '    $output = ob_get_clean();',
            '    return [\'output\' => $output];',
            '}',
            '',
            'function trace_route($route) {',
            '    global $app;',
            '    $menu = $app->getMenu();',
            '    $items = $menu->getItems();',
            '    foreach ($items as $item) {',
            '        if ($item->link == $route) {',
            '            $params = json_decode($item->params, true);',
            '            return [',
            '                \'itemid\' => (int)$item->id,',
            '                \'params\' => $params,',
            '                \'access\' => (int)$item->access',
            '            ];',
            '        }',
            '    }',
            '    return [\'error\' => \'Route not found in menu\'];',
            '}',
            '',
            'function get_api_token() {',
            '    // Generate API token for Super User',
            '    $db = \\Joomla\\CMS\\Factory::getDbo();',
            '    $query = $db->getQuery(true)',
            '        ->select(\'id\')',
            '        ->from(\'#__users\')',
            '        ->where(\'block = 0\')',
            '        ->where(\'sendEmail = 0\')',
            '        ->order(\'id ASC\')',
            '        ->setLimit(1);',
            '    ',
            '    $user_id = $db->setQuery($query)->loadResult();',
            '    ',
            '    if (!$user_id) {',
            '        return [\'error\' => \'No Super User found\'];',
            '    }',
            '    ',
            '    // Generate token (simplified - in real Joomla this would use proper token generation)',
            '    $token = bin2hex(random_bytes(32));',
            '    ',
            '    // Store token (this is simplified - real implementation would use Joomla\'s token system)',
            '    $db->setQuery(',
            '        $db->getQuery(true)',
            '            ->update(\'#__users\')',
            '            ->set(\'params = JSON_SET(params, "$.api_token", \' . $db->quote($token) . \')\')',
            '            ->where(\'id = \' . (int)$user_id)',
            '    )->execute();',
            '    ',
            '    return [\'token\' => $token, \'user_id\' => $user_id];',
            '}',
        ]
        return '\n'.join(php_lines)
