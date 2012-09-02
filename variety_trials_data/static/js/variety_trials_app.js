var variety_trials_app = {
	entryList: [],
	table: $('#debug'),
	locationList: [],
	cells: {},
	rows: {},
	columns: {},
	initSuggest: function() {},
	makeTable: function(){
		var zipcode=$('#js_zipcode').val()
		variety_trials_app.locationAjax(zipcode)
		
		var trial_entry = {
			// async: false,
			url: zipcode+'/last_three_years/json/',
			dataType: "json",
		}
		$.ajax(trial_entry).done(variety_trials_app.trialEntryList)
	},
	
	trialEntryList: function(response_data){
		for (i=0;i<response_data.length;i++)
		{
		variety_trials_app.populateTrialEntry(response_data[i])
		variety_trials_app.store_data(response_data[i])
		}
	},
	
	populateTrialEntry: function(response_data) {
		if($.inArray(response_data.fields.location, this.locationList)> -1){
				if($('.row'+response_data.fields.variety).length==0){// if there is no table row associated with the variety found in the response data, create one and populate it with the data in response_data
					this.table.append($('<tr class=row'+response_data.fields.variety+'>'))
					for (i=0;i<this.locationList.length;i++){// append a cell for each location
						$('.row'+response_data.fields.variety).append('<td class=column'+this.locationList[i]+'>')
					}
					$('.row'+response_data.fields.variety+' > td.column'+response_data.fields.location).text(response_data.fields.bushels_acre)
					var entryVariety = {//ajax call to get the name of the variety
						async: false,
						url: '/variety/'+response_data.fields.variety+'/json',
						dataType: "json",
					}
					$.ajax(entryVariety).done(variety_trials_app.populateVariety)
				}
			else{// if the table row already exists, populate the cell corresponding to the response_data
				$('.row'+response_data.fields.variety+' > td.column'+response_data.fields.location).text(response_data.fields.bushels_acre)
			}	
		}
	},
	
	store_data: function(response_data){
		cell_list=variety_trials_app.cells[response_data.fields.location,response_data.fields.variety]
		if(cell_list===undefined){
			var cell = new variety_trials_app.cell(response_data)
			variety_trials_app.cells[response_data.fields.location,response_data.fields.variety]=cell
			variety_trials_app.column(response_data.fields.location,cell)
			variety_trials_app.row(response_data.fields.variety,cell)
		}
		else{
			cell_list.add_cell(response_data)
			
		}
	},
	
	cell: function(response_data){
		this.data=new Array()
		
		this.add_cell=variety_trials_app.addcell
		this.data.push(response_data)
		
	},
	
	addcell: function(response_data){
		variety_trials_app.cells[response_data.fields.location,response_data.fields.variety].data.push(response_data)
	},
	
	row: function(va,current_cell){
		this.variety=va
		variety_trials_app.rows[this.variety]=[]
		add_cell(current_cell)
		function add_cell(cell){
			variety_trials_app.rows[variety_trials_app.row.variety]=cell
		}
	},
	
	column: function(loc,current_cell){
		this.location=loc
		variety_trials_app.columns[location]=[]
		add_cell(current_cell)
		function add_cell(cell){
			variety_trials_app.columns[variety_trials_app.column.location]=cell
		}
	},
	
	populateVariety: function(response_data){
		//prepends the name of the variety to the <tr> that has tha same id as the variety
		$('.row'+response_data[0].pk).prepend($('<th>').text=response_data[0].fields.name+response_data[0].pk)
	},
	
	populateLocation: function(response_data){
		// adds the eight closes locations to the table header and an array
		for (i=0;i<8;i++){
		$('.header').append($('<th class= column'+response_data[i].pk+'>').text(response_data[i].fields.name+response_data[i].pk))
		variety_trials_app.locationList.push(response_data[i].pk)}
	},
	
	locationAjax: function(zipcode){
		// ajax call to get the locations
		var entryLocation = {
			url: '/zipcode/near/'+zipcode+'/json/',
			async: false,
			dataType: "json",
		}

		$.ajax(entryLocation).done(variety_trials_app.populateLocation)
	},
	
	reorderTable: function(id1, id2){
			if(id1>id2){
			var dummy = id2
			id2 = id1
			id1 = dummy
			}
		row1=$('#debug > tr:nth-of-type('+id1+')')
		row2=$('#debug > tr:nth-of-type('+id2+')')
		row1.insertAfter(row2)
	},
	
	get_header_row: function(){
		head=  $('.header:nth-of-type(1)').clone()
		return head
		
	},
	
	get_lsd_row: function(){
		lsd= $('<tr>')
		return lsd
	},
	
	//removes a column, takes the id of the associated location as the argument
	remove_column: function(id){
		column=$('.column'+id)
		column.remove()
	},
	
	//exchanges the positions of two columns, takes the id of the associated locations as the arguments UNFINISHEDs
	swap_columns: function(id1, id2){
		if(id1>id2){
			var dummy = id2
			id2 = id1
			id1 = dummy
		}
		column1=$('.column'+id1)
		column2=$('.column'+id2)
		
	},
	
	testData: function(){
	console.log(variety_trials_app.cells)
	},
}; 
