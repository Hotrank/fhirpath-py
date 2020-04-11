import re
import json
import fhirpathpy.engine.util as util
import fhirpathpy.engine.nodes as nodes

# This file holds code to hande the FHIRPath Existence functions (5.1 in the
# specification).

intRegex = re.compile(r"^[+-]?\d+$")
numRegex = re.compile(r"^[+-]?\d+(\.\d+)?$")


def iif_macro(data, cond, ok, fail):
    if util.is_true(cond(data)):
        return ok(data)

    return fail(data)


def trace_fn(x, label=""):
    # print("TRACE:[" + label + "]", json.dumps(x))
    return x


def to_integer(coll):
    if len(coll) != 1:
        return []

    value = util.get_data(coll[0])

    if value == False:
        return 0

    if value == True:
        return 1

    if util.is_number(value):
        if int(value) == value:
            return value

        return []

    if str(value):
        if re.match(intRegex, value) is not None:
            return int(value)

        raise Exception("Could not convert to ineger: " + value)

    return []


def to_decimal(coll):
    if len(coll) != 1:
        return []

    value = util.get_data(coll[0])

    if value == False:
        return 0

    if value == True:
        return 1.0

    if util.is_number(value):
        return value

    if type(value) == str:
        if re.match(numRegex, value) is not None:
            return float(value)

        raise Exception("Could not convert to decimal: " + value)

    return []


def to_string(coll):
    if len(coll) != 1:
        return []

    value = util.get_data(coll[0])
    return str(value)


# Defines a function on engine called to+timeType (e.g., toDateTime, etc.).
# @param timeType The string name of a class for a time type (e.g. "FP_DateTime").


def to_date_time(coll):
    ln = len(coll)
    rtn = []
    if ln > 1:
        raise Exception("to_date_time called for a collection of length " + ln)

    if ln == 1:
        value = util.get_data(coll[0])

        t = nodes.FP_DateTime.check_string(value)

        if t:
            rtn[0] = t

    return rtn


def to_time(coll):
    ln = len(coll)
    rtn = []
    if ln > 1:
        raise Exception("to_time called for a collection of length " + ln)

    if ln == 1:
        value = util.get_data(coll[0])

        t = nodes.FP_Time.check_string(value)

        if t:
            rtn[0] = t

    return rtn
