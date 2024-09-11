function generateJSONFile() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();

  var positionSheet = spreadsheet.getSheetByName("position");
  var positionData = positionSheet.getRange(2, 1, positionSheet.getLastRow() - 1, positionSheet.getLastColumn()).getValues();

  var contentSheet = spreadsheet.getSheetByName("Content");
  var contentData = contentSheet.getRange(2, 1, contentSheet.getLastRow() - 1, contentSheet.getLastColumn()).getValues();

  var branchesSheet = spreadsheet.getSheetByName("Branches");
  var branchesData = branchesSheet.getRange(2, 1, branchesSheet.getLastRow() - 1, branchesSheet.getLastColumn()).getValues();

  var jsonData = {
    positions: []
  };

  for (var i = 0; i < positionData.length; i++) {
    var position = {
      heading: positionData[i][0],
      id: positionData[i][1],
      yrs_of_experience: positionData[i][2],
      number_of_positions: positionData[i][3],
      city: positionData[i][4],
      branches: []
    };

    if (position.city === "All") {
      for (var k = 0; k < branchesData.length; k++) {
        if (branchesData[k][0] !== "All") {
          var branch = {
            branch: branchesData[k][0],
            state: branchesData[k][1]
          };
          position.branches.push(branch);
        }
      }
    }

    for (var j = 0; j < contentData.length; j++) {
      if (positionData[i][0] === contentData[j][0]) {
        position.content = {
          primary_Responsibilities: contentData[j][1],
          knowledge_and_Skill_Requirements: contentData[j][2],
          education_and_Experience: contentData[j][3]
        };
        break;
      }
    }

    jsonData.positions.push(position);
  }

  var jsonString = JSON.stringify(jsonData, null, 2);

  var doc = DocumentApp.create('position_data');

  var docBody = doc.getBody();
  docBody.appendParagraph(jsonString);

  doc.saveAndClose();

  var fileId = doc.getId(); // Retrieve the ID of the file

  Logger.log('JSON document created. File ID: ' + fileId);
  SpreadsheetApp.getUi().alert('JSON document created. URL is: ' + doc.getUrl());
}
