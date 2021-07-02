function clearSheet() {
	const SPREADSHEET_ID: string = PropertiesService.getScriptProperties().getProperty('SPREADSHEET_ID');
	let SHEET_LIST: Array<string> = ['Log'];
	SHEET_LIST.forEach(function(element) {
		const SHEET = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName(element);
		SHEET.clear();
		if (SHEET.getFilter())
			SHEET.getFilter().remove();
	});
}
