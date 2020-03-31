TEMPLATE_START = """\
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
</head>
<style type="text/css">
#robot-summary-table {
    text-align: center;
    border-collapse: collapse;
  }
#robot-summary-table th {
      font-weight: normal;
      padding: 3px;
      background-color:#ddd;
      border: 1px solid black;
  }
#robot-summary-table td {
      font-weight: bold;
      margin: 0px;
      padding: 3px;
      border: 1px solid black;
  }

#robot-summary-table fail {
      color: #f00;
  }
#robot-summary-table pass {
      color: #0f0;
  }
</style>
<body leftmargin="8" marginwidth="0" topmargin="8" marginheight="4"  offset="0">
<h4><b>******************** Automation Results ******************</b></h4>
<p>
<b><h4>Test Statistics</h4></b>
"""
TEMPLATE_END = """</body>
</html>
"""
CITTABLE_TITLE="""<table id="robot-summary-table">
<tr>
<th><b>Type</b></th>
<th><b>Total</b></th>
<th><b>Run</b></th>
<th><b>No Run</b></th>
<th><b>Pass</b></th>
<th><b>Fail</b></th>
<th><b>ENB</b></th>
</tr>
"""
CITTABLE_END="""</p>
</table>
"""
CITTABLE_TR="""<tr>
<td>{}</td>
<td>{}</td>
<td>{}</td>
<td>{}</td>
<td><span style="color:green">{}</span></td>
<td><span style="color:red">{}</span></td>
<td>{}</td>
</tr>
"""

TEST_RESULT_TITLE="""<p>
<p/>
<div>
<table>
<tr><td><b>Test Execution Results</b></td></tr>
</table>
<table>
<tr style="background-color:#ddd">
<th>Test Name</th>
<th>Status</th>
<th>Tag</th>
</tr>
"""

TEST_RESULT_TD="""<tr>
<td>{}</td>
<td style="color: {} ? "#66CC00" : "#FF3333"">{}</td>
<td>{}</td>
</tr>
"""
TEST_RESULT_END="""</table>
</div>
"""
