function updateCluster(districts, data) {
  let district = districts.features;
  let numClusters = 4;
  for (let i = 0; i < district.length; i++) {
    let literacy = district[i].properties;
    let districtId = district[i].id.toLowerCase();
    if (data[districtId] !== undefined) {
      // priority considered color till columns corrected
      //console.log(lum);

      let normRisk = data[districtId]["Normalized_Log_Risk"];
      let clusterColor = "";
      if (normRisk >= 0.0 && normRisk < 0.2) {
        clusterColor = "#63ff00";
      } else if (normRisk >= 0.2 && normRisk < 0.4) {
        clusterColor = "#d6ff00";
      } else if (normRisk >= 0.4 && normRisk < 0.6) {
        clusterColor = "#ffff00";
      } else if (normRisk >= 0.6 && normRisk < 0.8) {
        clusterColor = "#ffc100";
      } else {
        clusterColor = "#ff0000";
      }

      let hoverValues = {
        pop: data[districtId].Population,
        pred: data[districtId]["Active_Cases_Predicted"],
        newPred: data[districtId]["New_Active_Cases_Predicted"],
        risk: data[districtId]["Normalized_Log_Risk"],
      };

      // literacy and maleliteracy considered as priority and color
      literacy.Literacy = hoverValues;
      literacy.MaleLiteracy = clusterColor;
    } else {
      // literacy and maleliteracy considered as priority and color
      literacy.Literacy = "NA";
      literacy.MaleLiteracy = "#63ff00";
    }
  }
}

function ColorLuminance(hex, lum) {
  // function returns color intensity of "hex"
  //based on "lum" in our case priority

  // validate hex string
  hex = String(hex).replace(/[^0-9a-f]/gi, "");
  if (hex.length < 6) {
    hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
  }
  lum = lum || 0;

  // convert to decimal and change luminosity
  var rgb = "#",
    c,
    i;
  for (i = 0; i < 3; i++) {
    c = parseInt(hex.substr(i * 2, 2), 16);
    c = Math.round(Math.min(Math.max(0, c + c * lum), 255)).toString(16);
    rgb += ("00" + c).substr(c.length);
  }
  console.log(rgb);
  return rgb;
}

export default updateCluster;
