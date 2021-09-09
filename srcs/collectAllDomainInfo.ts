function collectAllDomainInfo() {
	const SPREADSHEET_ID = PropertiesService.getScriptProperties().getProperty('SPREADSHEET_ID');
	const SHEET_LIST: Array<string> = ['バリュー', 'ムームー', 'お名前', 'バリュー（デブリ）', 'ムームー（デブリ）', 'お名前（デブリ）'];
	let allDomainInfo = [];
	try {
		SHEET_LIST.forEach(function(element) {
			allDomainInfo = allDomainInfo.concat(collectDomainInfo(SPREADSHEET_ID, element));
		});
		allDomainInfo.map((data, index) => data.unshift(index + 1));
		writeDomainInfo(SPREADSHEET_ID, allDomainInfo);
	} catch (e) {
		console.error(e.message);
	}
}

function collectDomainInfo(SPREADSHEET_ID, sheet: string) {
	const TARGET_SHEET = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName(sheet);
	const SERVER123_SSID = PropertiesService.getScriptProperties().getProperty('SERVER123_SSID');
	const URL_123 = `https://docs.google.com/spreadsheets/d/${SERVER123_SSID}/edit`;
	let checkDate: string = TARGET_SHEET.getRange('I1').getValue();
	let domainInfo: Array<Array<string>> = TARGET_SHEET.getRange(2, 2, TARGET_SHEET.getLastRow() - 1, 5).getValues()
		.filter(function(data) {
			let now = new Date();
			let today = new Date(`${now.getFullYear()}-${now.getMonth()+1}-${now.getDate()}`);
			let expiration_date = new Date(data[2]);
			return today <= expiration_date;
		})
		.map(data => data.concat(checkDate).concat(`=IF(COUNTIF(IMPORTRANGE("${URL_123}", "Main!F:F"), "${data[0]}"), TRUE, FALSE)`));
	return domainInfo;
}

function writeDomainInfo(SPREADSHEET_ID, allDomainInfo: Array<Array<string>>) {
	const TARGET_SHEET = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName('契約中ドメイン一覧');
	TARGET_SHEET.clear();
	if (TARGET_SHEET.getFilter())
		TARGET_SHEET.getFilter().remove();
	TARGET_SHEET.getRange('A1').setValue('No');
	TARGET_SHEET.getRange('B1').setValue('ドメイン名');
	TARGET_SHEET.getRange('C1').setValue('取得先');
	TARGET_SHEET.getRange('D1').setValue('有効期限');
	TARGET_SHEET.getRange('E1').setValue('自動更新\nフラグ');
	TARGET_SHEET.getRange('F1').setValue('自動更新\n管理対象');
	TARGET_SHEET.getRange('G1').setValue('チェック日');
	TARGET_SHEET.getRange('H1').setValue('123サーバー情報一覧存在確認')
		.setWrapStrategy(SpreadsheetApp.WrapStrategy.WRAP);
	TARGET_SHEET.getRange('I1').setValue('Size');
	TARGET_SHEET.getRange('J1').setValue(allDomainInfo.length);
	TARGET_SHEET.getRange('K1').setValue(Utilities.formatDate(new Date(), 'JST', 'yyyy-MM-dd'))
		.setBackground('#efefef');
	TARGET_SHEET.getRange('L1').setValue('=HYPERLINK("https://www.value-domain.com/login.php", "バリューへGo!!!")');
	TARGET_SHEET.getRange('M1').setValue('=HYPERLINK("https://muumuu-domain.com/?mode=conpane", "Go to ムームー")');
	TARGET_SHEET.getRange('N1').setValue('=HYPERLINK("https://navi.onamae.com/domain", "Go to お名前")');
	TARGET_SHEET.getRange('L1:N1').setFontWeight('bold');
	TARGET_SHEET.getRange('A1:I1').setBackground('#c9daf8');
	TARGET_SHEET.getRange('A1:J1').setFontWeight('bold');
	TARGET_SHEET.getRange('A1:N1')
		.setHorizontalAlignment('center')
		.setVerticalAlignment('middle')
		.setFontFamily('Meiryo');
	TARGET_SHEET.getRange('I1:J1')
		.setBorder(true, true, true, true, null, null, 'black', SpreadsheetApp.BorderStyle.SOLID);
	TARGET_SHEET.getRange(2, 1, allDomainInfo.length, 8).setValues(allDomainInfo).setFontFamily('Meiryo');
	TARGET_SHEET.getRange(2, 1, allDomainInfo.length, 1).setHorizontalAlignment('center');
	TARGET_SHEET.getRange(1, 1, TARGET_SHEET.getLastRow(), 8).createFilter();
	TARGET_SHEET.setFrozenRows(1);
	TARGET_SHEET.setRowHeight(1, 40);
	for (let col = 1; col <= 14; col++) {
		if (col == 1)
			TARGET_SHEET.setColumnWidth(col, 50);
		else if (col == 2)
			TARGET_SHEET.setColumnWidth(col, 200);
		else if (col == 8)
			TARGET_SHEET.setColumnWidth(col, 140);
		else if (col == 9 || col == 10)
			TARGET_SHEET.setColumnWidth(col, 70);
		else if (col >= 12 && col <= 14)
			TARGET_SHEET.setColumnWidth(col, 150);
		else
			TARGET_SHEET.setColumnWidth(col, 100);
	}
	const RANGE = TARGET_SHEET.getRange("H:H");
	const TRUE_RULE = SpreadsheetApp.newConditionalFormatRule()
		.whenTextEqualTo("TRUE")
  		.setFontColor("#1155cc")
  		.setBold(true)
		.setRanges([RANGE])
  		.build();
	const FALSE_RULE = SpreadsheetApp.newConditionalFormatRule()
		.whenTextEqualTo("FALSE")
  		.setFontColor("#FF0000")
  		.setBold(true)
		.setRanges([RANGE])
  		.build();
	TARGET_SHEET.setConditionalFormatRules([TRUE_RULE, FALSE_RULE]);
}
