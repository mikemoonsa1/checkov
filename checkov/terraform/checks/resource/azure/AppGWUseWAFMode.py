from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck


class AppGWUseWAFMode(BaseResourceCheck):
    def __init__(self):
        name = "Ensure that Application Gateway uses WAF in \"Detection\" or \"Prevention\" modes"
        id = "CKV_AZURE_122"
        supported_resources = ['azurerm_web_application_firewall_policy']
        categories = [CheckCategories.NETWORKING]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        if 'policy_settings' in conf and conf['policy_settings'][0]:
            policy_settings = conf['policy_settings'][0]
            self.evaluated_keys = ['policy_settings']
            if 'enabled' in policy_settings and not policy_settings['enabled'][0]:
                self.evaluated_keys = ['policy_settings/[0]/enable']
                return CheckResult.FAILED
        return CheckResult.PASSED


check = AppGWUseWAFMode()
