function doGet(e) {
  return HtmlService.createHtmlOutputFromFile('upload_portal');
}


function uploadCsvFile(contents, fileName) {
  var folderId = '1Mx_O-SkKX2z4bp9jN8bc1gGE0_APjQlA'; // Replace with your folder ID
  var archiveFolderId = '1WBNpIy3Crib5TR3nbnoFjwC4v0yPtnzu'; // Replace with your archive folder ID
  var folder = DriveApp.getFolderById(folderId);
  var archiveFolder = DriveApp.getFolderById(archiveFolderId);
  
  // Check for duplicate files
  var files = folder.getFilesByName(fileName);
  while (files.hasNext()) {
    var file = files.next();
    file.moveTo(archiveFolder);
  }
  
  // Upload new file
  var blob = Utilities.newBlob(contents, 'text/csv', fileName);
  var newFile = folder.createFile(blob);
  var csvData = Utilities.parseCsv(newFile.getBlob().getDataAsString());
  return csvData.length;
}
