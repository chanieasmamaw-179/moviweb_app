// util.js

function formatDate(date) {
    // Format a date as 'YYYY-MM-DD'
    let d = new Date(date);
    return d.toISOString().split('T')[0];
}

function logMessage(message) {
    console.log("Log: " + message);
}
