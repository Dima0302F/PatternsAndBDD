from steps.api_client import api_client

def before_scenario(context, scenario):
    """Setup before each scenario"""
    if not hasattr(context, 'client'):
        api_client(context)

def after_scenario(context, scenario):
    """Cleanup after each scenario"""
    if hasattr(context, 'client'):
        context.client.cleanup()
        context.client.reset()

def before_all(context):
    """Setup before all tests"""
    context.config.setup_logging()

def after_all(context):
    """Cleanup after all tests"""
    pass
