const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    projectId: "4hucyo",
    video: true,
    baseUrl: 'http://127.0.0.1:8000',
    "videoCompression": 32, // Compress video to a certain level
  "videoUploadOnPasses": false, // Only upload video if tests fail (if using a CI tool like CircleCI)
  "videosFolder": "cypress/videos",
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
