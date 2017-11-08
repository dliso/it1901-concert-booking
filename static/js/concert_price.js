const print = console.log;

let form = document.getElementById("create-concert-form");

if (form === null) {
    form = document.forms[0];
}

function handleFormChange(event) {
  const stage_info_string = document.getElementById("stage_info").innerHTML;
  const stage_info = JSON.parse(stage_info_string);
  const stage_info_map = new Map(stage_info.map(stage=>{
    return [stage.pk.toString(), stage]
  }));
    const priceField =
          document.getElementById("id_ticket_price") ||
          document.getElementById("id_price")
          ;
    const stageField =
          document.getElementById("id_stage_name") ||
          document.getElementById("id_stage")
          ;
  const selectedStage = stage_info_map.get(stageField.value);
    if (event.target === stageField) {
        priceField.value = (selectedStage.fields.stage_costs*1.5)/selectedStage.fields.num_seats;
      //Formula calculating an example ticket prize
      //(Total costs + profit)/Total tickets
    }
  }

form.addEventListener("change", handleFormChange);
