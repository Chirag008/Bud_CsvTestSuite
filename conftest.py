import pytest

default_html_path = 'reports/report.html'


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    if not config.option.htmlpath:
        config.option.htmlpath = default_html_path


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call":
        # extra.append(pytest_html.extras.html("<div>Additional HTML</div>"))
        # report.extra = extra
        pass
