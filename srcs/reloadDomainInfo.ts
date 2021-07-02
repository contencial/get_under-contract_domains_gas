function reloadDomainInfo() {
	let confirmation = Browser.msgBox('契約中ドメイン再読込', '本当に実行しますか？', Browser.Buttons.OK_CANCEL);
	if (confirmation == "cancel") {
		return;
	}
	try {
		getDomainInfo();
	} catch (e) {
		Browser.msgBox(e.message);
	}
}
