(() => {
  const form = document.querySelector("#rfq-form");
  const outputSection = document.querySelector("#rfq-output-section");
  const output = document.querySelector("#rfq-output");
  const status = document.querySelector("#rfq-status");
  if (!form || !outputSection || !output || !status) return;

  const value = (name, fallback = "Not specified") => {
    const field = form.elements.namedItem(name);
    const result = field && typeof field.value === "string" ? field.value.trim() : "";
    return result || fallback;
  };

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const product = value("product");
    const brief = [
      `REQUEST FOR QUOTATION: ${product}`,
      "",
      "PRODUCT AND REQUIREMENTS",
      `Product / project: ${product}`,
      `Specification, revision or reference: ${value("specification")}`,
      `Quantity tiers: ${value("quantities")}`,
      `Target market and destination: ${value("destination")}`,
      `Delivery term and named place: ${value("delivery")}`,
      `Packaging, labels and cartons: ${value("packaging")}`,
      `Quality checks and acceptance criteria: ${value("quality")}`,
      `Buyer-specified tests, standards or documents: ${value("documents")}`,
      `Sample, timing and other constraints: ${value("timing")}`,
      `Requested quote return date: ${value("due")}`,
      "",
      "PLEASE INCLUDE IN YOUR RESPONSE",
      "1. Unit price for every requested quantity and currency.",
      "2. MOQ, tooling, setup and other one-time costs as separate line items.",
      "3. Sample cost, sample lead time and production lead time.",
      "4. Included work, exclusions, assumptions and any proposed deviations.",
      "5. Packaging details, carton dimensions, gross weight and pack quantity.",
      "6. Evidence for the buyer-specified tests, standards or documents, including scope and validity where applicable.",
      "7. Proposed payment terms, quotation validity, and delivery term with named place and version.",
      "",
      "Please identify any requirement that cannot be met and state the alternative clearly. Do not silently substitute specifications or components.",
      "",
      "This brief records buyer-provided requirements. It does not determine legal, customs, safety or certification requirements."
    ].join("\n");
    output.textContent = brief;
    outputSection.hidden = false;
    status.textContent = "Draft created in this browser. Review it before copying or downloading.";
    outputSection.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  document.querySelector("#copy-rfq")?.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(output.textContent || "");
      status.textContent = "RFQ brief copied to your clipboard.";
    } catch {
      output.focus();
      status.textContent = "Clipboard access was unavailable. Select the brief above and copy it manually.";
    }
  });

  document.querySelector("#download-rfq")?.addEventListener("click", () => {
    const product = value("product", "china-supplier-rfq").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "china-supplier-rfq";
    const blob = new Blob([output.textContent || ""], { type: "text/plain;charset=utf-8" });
    const link = document.createElement("a");
    const objectUrl = URL.createObjectURL(blob);
    link.href = objectUrl;
    link.download = `${product}-rfq.txt`;
    link.click();
    window.setTimeout(() => URL.revokeObjectURL(objectUrl), 1000);
    status.textContent = "RFQ brief downloaded to your device.";
  });
})();
