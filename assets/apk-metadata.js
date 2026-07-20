(() => {
  const endpoint = `assets/apk-metadata.json?t=${Date.now()}`;
  const fallbackFileName = "Listooo-version 139 (1.2.15).apk";

  const versionLabels = document.querySelectorAll(".apk-version");
  const downloadButtons = document.querySelectorAll(".apk-download-button");

  const showFileName = (fileName) => {
    versionLabels.forEach((label) => {
      label.textContent = fileName;
    });
  };

  showFileName(fallbackFileName);

  fetch(endpoint, {
    method: "GET",
    headers: { accept: "application/json" },
    cache: "no-store",
  })
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then((metadata) => {
      if (
        typeof metadata.fileName !== "string" ||
        !metadata.fileName.toLowerCase().endsWith(".apk")
      ) {
        return;
      }

      showFileName(metadata.fileName);
      if (typeof metadata.viewUrl === "string" && metadata.viewUrl) {
        downloadButtons.forEach((button) => {
          button.href = metadata.viewUrl;
        });
      }
    })
    .catch(() => {
      // Keep the last known APK filename when Drive is temporarily unavailable.
    });
})();
