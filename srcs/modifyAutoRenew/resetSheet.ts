function manualResetSheet() {
	let confirmation = Browser.msgBox('パラメータリセット', '本当に実行しますか？', Browser.Buttons.OK_CANCEL);
	if (confirmation == "cancel") {
		return;
	}
	resetSheet();
}

function resetSheet() {
    const SPREADSHEET_ID = PropertiesService.getScriptProperties().getProperty('SPREADSHEET_ID');
    const PARAM_SHEET = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName('自動更新変更ツール');
    PARAM_SHEET.clear();
	if (PARAM_SHEET.getFilter())
		PARAM_SHEET.getFilter().remove();
    PARAM_SHEET.getRange('A1').setValue('ドメイン').setBackground('#a4c2f4');
    PARAM_SHEET.getRange('B1').setValue('取得・変更数').setBackground('#f9cb9c');
    PARAM_SHEET.getRange('B2').setValue('=ArrayFormula(match(0,len(A:A),0))-2')
			.setFontWeight('bold')
			.setHorizontalAlignment('center');
    PARAM_SHEET.getRange('B1:B2')
		.setBorder(true, true, true, true, null, null, 'black', SpreadsheetApp.BorderStyle.DOUBLE);
    PARAM_SHEET.getRange('F1').setValue('結果');
    PARAM_SHEET.getRange('G1').setValue('ドメインID');
    PARAM_SHEET.getRange('H1').setValue('ドメイン名');
    PARAM_SHEET.getRange('I1').setValue('自動更新設定');
    PARAM_SHEET.getRange('J1').setValue('自動更新ドメイン\n全体設定');
    PARAM_SHEET.getRange('K1').setValue('自動更新ドメイン\n個別設定');
	PARAM_SHEET.getRange('F1:K1').setBackground('#ffe599');
    PARAM_SHEET.getRange('A1:K1').setFontWeight('bold')
			.setHorizontalAlignment('center')
			.setVerticalAlignment('middle');
    PARAM_SHEET.getRange('A1:K100').setFontFamily('Meiryo');
    PARAM_SHEET.getRange('C14').setValue('※注意')
		.setFontWeight('bold')
		.setFontColor('red')
		.setHorizontalAlignment('right');
	for (let col = 1; col <= 11; col++) {
		if (col == 1 || (col >= 8 && col <= 11))
			PARAM_SHEET.setColumnWidth(col, 150);
		else
			PARAM_SHEET.setColumnWidth(col, 100);
	}
   PARAM_SHEET.setRowHeight(1, 40);
}
