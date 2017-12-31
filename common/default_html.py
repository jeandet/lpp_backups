html_body = """
<html>
    <head>
    <style>
        table {{
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
        }}

        td, th {{
            border: 2px solid #000000;
            text-align: left;
            padding: 8px;
        }}

        tr:nth-child(even) {{
            background-color: #dddddd;
        }}
    </style>
    </head>
    <body>
        <div>
            {html_backup}
        </div>
        <div>
            {html_monitor}
        </div>
    </body>
</html>
"""

html_backup = """
<table>
  <tr>
    <th>Step name</th>
    <th>backup output</th>
    <th>Status</th>
    <th>File size</th>
  </tr>
  {html_backup_steps}
</table>
"""

html_backup_step = """
  <tr>
    <td>{name}</th>
    <td>{output}</th>
    <td>{status}</th>
    <td>{size}</th>
  </tr>
"""

html_monitor = """
<ul>
    {html_monitor_elements}
</ul>
"""

html_monitor_element = """
<li>{name}
    <ul>
      <li>Usage: {usage} on {available} available ({free} free)</li>
    </ul>
</li>
"""

html_success='<font color="green">Success</font>'
html_fail='<font color="red">Failed</font>'
