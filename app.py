from flask import abort, Flask, jsonify, request
from DerTodInVenedig.converter import read_data_to_df

app = Flask(__name__)

MORT_DATA = read_data_to_df('data/RatesDeaths_AllIndicators.xlsx')


@app.route('/mortality_rate', methods=['GET'])
def mortality_rate():
    """  
    "http://0.0.0.0:8080/mortality_rate?country_code=DEU&year=1970&year=1971&mr_type=U5MR0"
    """
    country_code = request.args.get('country_code')
    year_from = request.args.get('year_from')
    year_to = request.args.get('year_to')
    mr_type = request.args.get('mr_type')
    try:
        validate(country_code, year_from, year_to, mr_type)
    except AssertionError:
        # cannot process
        return abort(422)
    data = query_data(country_code, year_from, year_to, mr_type)
    return jsonify(data)


# backend section #
def validate(country_code, year_from, year_to, mr_type):
    """
    Validates args to prevent pandas Attribute error later
    """
    assert year_from < year_to
    assert MORT_DATA.index.get_level_values(0).contains(country_code)
    assert MORT_DATA.index.get_level_values(1).contains(year_from)
    assert MORT_DATA.index.get_level_values(1).contains(year_to)
    assert mr_type in MORT_DATA.columns


def query_data(country_code, year_from, year_to, mr_type):
    data = MORT_DATA[mr_type][country_code][year_from:year_to].mean()
    # FIXME  WHAT TO DO WITH NaN?
    return {'avg_value': data}
