function manualCreateDomainTarget() {
	let confirmation = Browser.msgBox('ドメインリスト抽出処理', '本当に実行しますか？', Browser.Buttons.OK_CANCEL);
	if (confirmation == "cancel") {
		return ;
	}
	createDomainTarget();
}

function createDomainTarget() {
	const SPREADSHEET_ID = PropertiesService.getScriptProperties().getProperty('SPREADSHEET_ID');
	const SHEET = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName('自動更新変更ツール');

	resetSheet();
	let targetDomainList: Array<Array<string>>;
	targetDomainList = getDomainTarget()
	if (targetDomainList.length < 1)
		return ;
	SHEET.getRange(2, 1, targetDomainList.length, 1)
		.setValues(targetDomainList)
		.setFontFamily('Meiryo');
}

function getDomainTarget() {
	const SPREADSHEET_ID = PropertiesService.getScriptProperties().getProperty('SPREADSHEET_ID');
	const TARGET_SHEET = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName('ドメイン自動更新管理');
	
	const LAST_ROW = TARGET_SHEET.getLastRow();
	let domainList: Array<Array<string>> = TARGET_SHEET.getRange(`A4:M${LAST_ROW}`).getValues();
	domainList = domainList.filter(data => data[10] == 'OFF' && data[2] == 'バリュー' && data[12] == '自動')
		.map(data => [data[1]]);
	return domainList;
}
