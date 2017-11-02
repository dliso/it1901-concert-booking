const print = console.log;

const form = document.getElementById("create-concert-form");

function handleFormChange(event) {
  const stage_info_string = document.getElementById("stage_info").innerHTML;
  const stage_info = JSON.parse(stage_info_string);
  const stage_info_map = new Map(stage_info.map(stage=>{
    return [stage.pk.toString(), stage]
  }));
  const priceField = document.getElementById("id_ticket_price");
  const stageField = document.getElementById("id_stage_name");
  const selectedStage = stage_info_map.get(stageField.value);
    if (event.target !== priceField) {
        priceField.value = (selectedStage.fields.stage_costs*1.5)/selectedStage.fields.num_seats;
      //Formula calculating an example ticket prize
      //(Total costs + profit)/Total tickets
    }
  }

form.addEventListener("change", handleFormChange);
