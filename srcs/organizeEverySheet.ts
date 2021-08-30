function oraganizeEverySheet() {
	const SPREADSHEET_ID = PropertiesService.getScriptProperties().getProperty('SPREADSHEET_ID');
	const UNDER_CONTRACT_LIST: Array<string> = ['ムームー', 'お名前', 'ムームー（デブリ）', 'お名前（デブリ）'];
	UNDER_CONTRACT_LIST.forEach(function(element) {
		formatUnderContractSheet(SPREADSHEET_ID, element);
	});
	const REGISTERED_LIST: Array<string> = ['登録中ドメイン（FTPサーバー）', '登録中ドメイン（123サーバー）'];
	REGISTERED_LIST.forEach(function(element) {
		formatRegisteredSheet(SPREADSHEET_ID, element);
	});
}

function formatUnderContractSheet(SPREADSHEET_ID, sheet: string) {
	const TARGET_SHEET = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName(sheet);
	if (TARGET_SHEET.getFilter())
		TARGET_SHEET.getFilter().remove();
	TARGET_SHEET.getRange('A1:G1').setBackground('#c9daf8');
	TARGET_SHEET.getRange('I1').setBackground('#efefef');
	TARGET_SHEET.getRange('A1:H1').setFontWeight('bold');
	TARGET_SHEET.getRange('J1').setFontWeight('bold');
	TARGET_SHEET.getRange('A1:J1')
		.setHorizontalAlignment('center')
		.setVerticalAlignment('middle')
		.setFontFamily('Meiryo');
	TARGET_SHEET.getRange('G1:H1')
		.setBorder(true, true, true, true, null, null, 'black', SpreadsheetApp.BorderStyle.SOLID);
	TARGET_SHEET.getRange(1, 1, TARGET_SHEET.getLastRow(), 6)
		.setFontFamily('Meiryo')
		.createFilter();
	TARGET_SHEET.getRange(2, 1, TARGET_SHEET.getLastRow(), 1).setHorizontalAlignment('center');
	TARGET_SHEET.setFrozenRows(1);
	TARGET_SHEET.setRowHeight(1, 40);
	for (let col = 1; col <= 10; col++) {
	    if (col == 1)
	        TARGET_SHEET.setColumnWidth(col, 50);
		else if (col == 2)
	        TARGET_SHEET.setColumnWidth(col, 200);
	    else if (col == 7 || col == 8)
	        TARGET_SHEET.setColumnWidth(col, 70);
		else if (col == 10)
	        TARGET_SHEET.setColumnWidth(col, 150);
	    else
	        TARGET_SHEET.setColumnWidth(col, 100);
	}
}

function formatRegisteredSheet(SPREADSHEET_ID, sheet: string) {
	const TARGET_SHEET = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName(sheet);
	if (TARGET_SHEET.getFilter())
		TARGET_SHEET.getFilter().remove();
	TARGET_SHEET.getRange('A1:D1').setBackground('#c9daf8');
	TARGET_SHEET.getRange('J1').setBackground('#efefef');
	TARGET_SHEET.getRange('A1:I1').setFontWeight('bold');
	TARGET_SHEET.getRange('K1').setFontWeight('bold');
	TARGET_SHEET.getRange('A1:K1')
		.setHorizontalAlignment('center')
		.setVerticalAlignment('middle')
		.setFontFamily('Meiryo');
	TARGET_SHEET.getRange('D1:E1')
		.setBorder(true, true, true, true, null, null, 'black', SpreadsheetApp.BorderStyle.SOLID);
	TARGET_SHEET.getRange(1, 1, TARGET_SHEET.getLastRow(), 3)
		.setFontFamily('Meiryo')
		.createFilter();
	TARGET_SHEET.getRange(2, 1, TARGET_SHEET.getLastRow(), 1).setHorizontalAlignment('center');
	TARGET_SHEET.getRange(2, 3, TARGET_SHEET.getLastRow(), 1).setHorizontalAlignment('center');
	TARGET_SHEET.setFrozenRows(1);
	TARGET_SHEET.setRowHeight(1, 40);
	for (let col = 1; col <= 11; col++) {
	    if (col == 1)
	        TARGET_SHEET.setColumnWidth(col, 110);
		else if (col == 2)
	        TARGET_SHEET.setColumnWidth(col, 200);
	    else if (col == 3)
	        TARGET_SHEET.setColumnWidth(col, 120);
		else if (col == 4 || col == 5)
	        TARGET_SHEET.setColumnWidth(col, 70);
		else if (col >= 6 && col <= 9)
	        TARGET_SHEET.setColumnWidth(col, 50);
	    else if (col == 11)
	        TARGET_SHEET.setColumnWidth(col, 140);
	    else
	        TARGET_SHEET.setColumnWidth(col, 100);
	}
}
