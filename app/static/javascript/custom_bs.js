initBSTooltips();
dismissAlertAfterTimeout();

function initBSTooltips() {
	const tooltipTriggerList = [].slice.call(
		document.querySelectorAll('[data-bs-toggle="tooltip"]')
	);
	tooltipTriggerList.map(function (tooltipTriggerEl) {
		return new bootstrap.Tooltip(tooltipTriggerEl);
	});
}

function dismissAlert() {
	var alert = document.querySelector(".alert");
	if (alert) {
		alert.style.display = "none";
	}
}

function dismissAlertAfterTimeout() {
	setTimeout(dismissAlert, 5000);
}