from datetime import datetime, date


def init_template_filters(app):
    @app.template_filter("yes_no")
    def yesno_format(value):
        if value is None:
            return ""
        if value:
            return "Yes"
        else:
            return "No"

    @app.template_filter("datetime_format")
    def datetime_format(value):
        if value:
            return value.strftime("%c")
        else:
            return ""

    @app.template_filter("nbsp")
    def nbsp(value):
        if value:
            return value.replace(' ', '\xa0')
        else:
            return ""

    @app.template_filter("date_format")
    def date_format(value):
        if value is None:
            return ''
        if value and (isinstance(value, date) or isinstance(value, datetime)):
            return value.strftime("%-d %b %Y")
        else:
            return value

    @app.template_filter("blank_if_none")
    def blank_if_none(value):
        return value or ""

    @app.template_filter("default_if_none")
    def default_if_none(value, default):
        return value or default

    @app.template_filter("currency")
    def currency(value):
        if value:
            return "£{:.2f}".format(value)
        else:
            return ""

    @app.template_filter("separated_number")
    def currency(value):
        return F"{value:,}"

    @app.template_filter("title_case")
    def currency(value):
        return value.title()

    @app.context_processor
    def inject_now():
        return {'current_year': datetime.utcnow().strftime("%Y")}
