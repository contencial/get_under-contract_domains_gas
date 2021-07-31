function modifyAutoRenewON() {
	let confirmation = Browser.msgBox('自動更新設定ON', '本当に実行しますか？', Browser.Buttons.OK_CANCEL);
	if (confirmation == "cancel") {
		return;
	}
	modifyAutoRenew(10);
}

function modifyAutoRenewOFF() {
	let confirmation = Browser.msgBox('自動更新設定OFF', '本当に実行しますか？', Browser.Buttons.OK_CANCEL);
	if (confirmation == "cancel") {
		return;
	}
	modifyAutoRenew(0);
}

function modifyAutoRenew(autoRenewFlag: int) {
	const SPREADSHEET_ID = PropertiesService.getScriptProperties().getProperty('SPREADSHEET_ID');
	const PARAM_SHEET = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName('自動更新変更ツール');
	const SIZE_CELL = PARAM_SHEET.getRange('B2');
	let loopSize: number = SIZE_CELL.getValue();
	try {
		if (SIZE_CELL.isBlank() || typeof loopSize != 'number' || loopSize < 0)
			throw new Error('Parameter Error: 変更数に誤りがあります。');
		for (let i = 1; i <= loopSize; i++) {
			const DOMAIN_CELL = PARAM_SHEET.getRange(1 + i, 1);
			let domain: string = DOMAIN_CELL.getValue();
			if (DOMAIN_CELL.isBlank() || typeof domain != 'string')
				throw new Error('Parameter Error: ドメインに誤りがあります。');
			putMethodApi(domain, 1 + i, PARAM_SHEET, autoRenewFlag);
		}
	} catch (e) {
		console.log(e.message);
		Browser.msgBox(e.message);
	}
}

function putMethodApi(domain: string, row: number, param_sheet: Sheet, autoRenewFlag: int) {
	const VALUE_DOMAIN_URL: string = `https://api.value-domain.com/v1/domains/${domain}/autorenew`;
	const API_KEY: string = PropertiesService.getScriptProperties().getProperty('API_KEY');
	let options = {
		headers: {
			'Authorization': 'Bearer ' + API_KEY
		},
		method: 'put',
		contentType: 'application/json',
		payload: JSON.stringify({autorenew_all: 0, autorenew_domain: autoRenewFlag}),
		muteHttpExceptions: true
	};
	try {
		let response = UrlFetchApp.fetch(VALUE_DOMAIN_URL, options);
		console.log(response.getResponseCode());
		let result = JSON.parse(response.getContentText());
		param_sheet.getRange(row, 6, 1, 6).setFontSize(10).setFontFamily('Meiryo');
		let status = param_sheet.getRange(row, 6);
		status.setValue(response.getResponseCode())
			.setFontWeight('bold')
			.setHorizontalAlignment('center');
		if (response.getResponseCode() === 200) {
			status.setFontColor('#1155cc');
			param_sheet.getRange(row, 7).setValue(result.results.domainid);
			param_sheet.getRange(row, 8).setValue(result.results.domainname);
			param_sheet.getRange(row, 9).setValue(result.results.autorenew);
			param_sheet.getRange(row, 10).setValue(result.results.autorenew_all);
			param_sheet.getRange(row, 11).setValue(result.results.autorenew_domain);
			param_sheet.getRange(row, 9, 1, 3).setFontColor(null).setFontWeight(null);
		} else {
			status.setFontColor('#f13503');
			param_sheet.getRange(row, 7).setValue(result.errors.domainid);
			param_sheet.getRange(row, 8).setValue(result.errors.domainname);
			param_sheet.getRange(row, 9.setValue(result.errors.message)
						.setFontColor('#f13503')
						.setFontWeight('bold');
			param_sheet.getRange(row, 10).setValue('');
			param_sheet.getRange(row, 11).setValue('');
		}
		console.log(response.getContentText());
	} catch (e) {
		console.log(e.message);
	}
}
