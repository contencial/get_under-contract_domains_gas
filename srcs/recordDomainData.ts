function recordDomainData() {
	try {
		const SPREADSHEET_ID = PropertiesService.getScriptProperties().getProperty('SPREADSHEET_ID');
		const SHEET_123 = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName('登録中ドメイン（123サーバー）');
		const SHEET_FTP = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName('登録中ドメイン（FTPサーバー）');
		const SHEET_DOMAIN = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName('契約中ドメイン一覧');

		const REGISTERED_NUM_123 = SHEET_123.getRange('E1').getValue();
		const REGISTERED_NUM_FTP = SHEET_FTP.getRange('E1').getValue();
		const LAST_ROW_DOMAIN: number = SHEET_DOMAIN.getLastRow();
		const DOMAIN_DATA = SHEET_DOMAIN.getRange(`C2:C${LAST_ROW_DOMAIN}`).getValues();
		const TOTAL = DOMAIN_DATA.length;
		const VALUE = DOMAIN_DATA.filter(data => data[0] == 'バリュー').length;
		const MUUMUU = DOMAIN_DATA.filter(data => data[0] == 'ムームー').length;
		const ONAMAE = DOMAIN_DATA.filter(data => data[0] == 'お名前').length;
		const VALUE_DEBRIS = DOMAIN_DATA.filter(data => data[0] == 'バリュー（デブリ）').length;
		const MUUMUU_DEBRIS = DOMAIN_DATA.filter(data => data[0] == 'ムームー（デブリ）').length;
		const ONAMAE_DEBRIS = DOMAIN_DATA.filter(data => data[0] == 'お名前（デブリ）').length;

		const SERVER123_SSID = PropertiesService.getScriptProperties().getProperty('SERVER123_SSID');
		const SHEET_SERVER123 = SpreadsheetApp.openById(SERVER123_SSID).getSheetByName('Main');
		const UNDER_MANAGEMENT_NUM = SHEET_SERVER123.getRange('B1').getValue();

		const RECORD_SSID = PropertiesService.getScriptProperties().getProperty('RECORD_SSID');
		const SHEET = SpreadsheetApp.openById(RECORD_SSID).getSheetByName('DomainRecord');
		const LAST_ROW: number = SHEET.getLastRow();
		SHEET.getRange(`A${LAST_ROW + 1}`).setValue(Utilities.formatDate(new Date(), 'JST', 'yyyy/MM/dd'));
		SHEET.getRange(`B${LAST_ROW + 1}`).setValue(UNDER_MANAGEMENT_NUM);
		SHEET.getRange(`C${LAST_ROW + 1}`).setValue(REGISTERED_NUM_123);
		SHEET.getRange(`D${LAST_ROW + 1}`).setValue(REGISTERED_NUM_FTP);
		SHEET.getRange(`E${LAST_ROW + 1}`).setValue(TOTAL);
		SHEET.getRange(`F${LAST_ROW + 1}`).setValue(VALUE);
		SHEET.getRange(`G${LAST_ROW + 1}`).setValue(MUUMUU);
		SHEET.getRange(`H${LAST_ROW + 1}`).setValue(ONAMAE);
		SHEET.getRange(`I${LAST_ROW + 1}`).setValue(VALUE_DEBRIS);
		SHEET.getRange(`J${LAST_ROW + 1}`).setValue(MUUMUU_DEBRIS);
		SHEET.getRange(`K${LAST_ROW + 1}`).setValue(ONAMAE_DEBRIS);
		SHEET.getRange(`A${LAST_ROW + 1}:K${LAST_ROW + 1}`)
			.setFontFamily('Meiryo')
			.setHorizontalAlignment('center');
	} catch (e) {
		console.error(e.message);
	}
}
