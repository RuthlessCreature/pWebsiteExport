(() => {
  const list = document.querySelector("[data-checklist]");
  if (!list) return;
  const rows = [...list.querySelectorAll("[data-check-row]")];
  const reviewed = document.querySelector("[data-reviewed]");
  const followUps = document.querySelector("[data-follow-up]");
  const criticalOpen = document.querySelector("[data-critical-open]");
  const statusMessage = document.querySelector("[data-export-status]");

  const refresh = () => {
    const states = rows.map((row) => ({
      row,
      status: row.querySelector("[data-status]").value,
      critical: row.dataset.critical === "true",
    }));
    const done = states.filter((item) => item.status !== "not-reviewed").length;
    const follow = states.filter((item) => item.status === "follow-up" || item.status === "concern").length;
    const openCritical = states.filter((item) => item.critical && item.status !== "evidence-recorded").length;
    reviewed.textContent = String(done);
    followUps.textContent = String(follow);
    criticalOpen.textContent = String(openCritical);
    rows.forEach((row) => {
      const select = row.querySelector("[data-status]");
      row.dataset.state = select.value;
    });
  };

  rows.forEach((row) => row.querySelector("[data-status]").addEventListener("change", refresh));
  document.querySelector("[data-export]").addEventListener("click", () => {
    const records = [["Category", "Check item", "Evidence requested", "Critical", "Review status", "Notes"]];
    rows.forEach((row) => {
      records.push([
        row.dataset.category,
        row.dataset.item,
        row.dataset.evidence,
        row.dataset.critical === "true" ? "Yes" : "No",
        row.querySelector("[data-status]").selectedOptions[0].textContent.trim(),
        row.querySelector("textarea").value.trim(),
      ]);
    });
    const quote = (value) => `"${String(value).replaceAll('"', '""')}"`;
    const csv = records.map((record) => record.map(quote).join(",")).join("\r\n");
    const blob = new Blob(["\ufeff", csv], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "china-supplier-verification-review.csv";
    link.click();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    statusMessage.textContent = "Your review CSV was generated in this browser. It was not uploaded.";
  });
  refresh();
})();
