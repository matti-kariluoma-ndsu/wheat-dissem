function variety_trials__init_handsontable(column_length, headers, input_container, output_container)
{
	
	var variety_trials__sheet = $(input_container)
	var variety_trials__output = $(output_container)
	
	function variety_trials__update_form(changes)
	{
		var rows = []
		rows.push(headers);
		var table = variety_trials__sheet.handsontable('getData');
		var row;
		for (i=0; i < table.length; i++)
		{
			row = table[i];
			rows.push(row);
		}
		variety_trials__output.val(JSON.stringify(rows));
	}
	
	variety_trials__sheet.handsontable({
		startRows: 2,
		startCols: column_length,
		minSpareRows: 1,
		contextMenu: true,
		rowHeaders: true,
		colHeaders: headers,
		onChange: variety_trials__update_form
	});

}
