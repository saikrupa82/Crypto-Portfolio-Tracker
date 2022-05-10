var search_bar = document.getElementById("search_coin");
search_bar.onkeyup = () => {
	console.log(search_bar.value)
	show_search();
}



function Tpop(){
	let tpopup = document.getElementById("Tpopup");
	let rpopup = document.getElementById("Rpopup");
	tpopup.style.display = "flex";
	rpopup.style.display = "none";
}

function Rpop(){
	let rpopup = document.getElementById("Rpopup");
	let tpopup = document.getElementById("Tpopup");
	rpopup.style.display = "flex";
	tpopup.style.display = "none";
}
function closepopup(){
	let rpopup = document.getElementById("Rpopup");
	let tpopup = document.getElementById("Tpopup");
	rpopup.style.display = "none";
	tpopup.style.display = "none";
}
async function show_search(){
	results=document.getElementById("results");
	tosearch=document.getElementById("search_coin").value;
	ele='';
	
	if(tosearch==""){
		results.style.display = "none";
	}
	else{
		  const idsdata = await fetch(`https://api.coingecko.com/api/v3/search?query=${tosearch}`);
	      const idsresponse = await idsdata.json();
	      const ids=[]; 
	      if(idsresponse.coins.length>10){

	      	for(let i=0;i<10;i++){
	      		ids.push(idsresponse.coins[i].id);
	      	}
	      }
	      else{
	      	//add else later
	      }
	      ids.map(id => {
	      	ele+=`<button
                              type="button"
                              class="list-group-item list-group-item-action"
                              onclick=set('${id}')
                            >
                              ${id}
                            </button>`;
	      });
	      results.innerHTML=ele;
	}
	
	results.style.display = "block";
	
}
async function set(coin){
	document.getElementById("search_coin").value = coin;
	document.getElementById("results").style.display="none";
	document.getElementById("coin_symbol").style.display = "hidden";
	const coin_details_temp = await fetch(`https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids=${coin}&order=market_cap_desc&per_page=100&page=1&sparkline=false`);
	const coin_details = await coin_details_temp.json();
	const price = coin_details[0].current_price;
	const symbol = coin_details[0].symbol;
	const datee = coin_details[0].last_updated.slice(0,10);
	document.getElementById("price").value = price;
	document.getElementById("date").value = datee;
	document.getElementById("coin_symbol").value = symbol;
}
function temp(val){
	console.log(val);
}

