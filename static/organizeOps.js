/* Dumb code to use in emergencies
var showOpps = function(e) {
    var desc = document.getElementById("descriptions");
    desc.innerHTML = e.target.innerHTML;
}

var hideOpps = function() {
    var desc = document.getElementById("descriptions");
    desc.innerHTML = "";
}

console.log(`num_desc = ${document.getElementsByClassName("desc").length}`);
console.log(`cols = ${document.getElementsByTagName("table")[0].rows.length}`);

for(var i = 0; i < 11; i++) {
    //for(var i = 0; i < document.getElementsByClassName("desc").length; i++) {
    console.log(`desc[${i}]`);
    document.getElementsByClassName("desc")[i].addEventListener("mouseover", showOpps); //() => {showOpps});
    document.getElementsByClassName("desc")[i].addEventListener("mouseout", hideOpps); //() => {showOpps(this);});
}

console.log("die in hell");
*/

//Goal: Sort element by getting 
var order = document.getElementById("order").value;
var rows = document.getElementsByTagName("table")[0].rows;
var arr_rows = Array.from(table.rows);

document.getElementById("order").addEventListener("change", libero);

var merge_sorth = function(cell_num, compare) {
    //l starts at one because row 0 is header
    merge_sort(cell_num, compare, 1, rows.length);
}

var merge_sort = function(cell_num, compare, l, r) {
    if(l < r) {
        var m = (l + r) / 2;
        merge_sort(cell_num, compare, l, m);
        merge_sort(cell_num, compare, m, r);
        merge(cell_num, compare, l, m, r);
    }
}

var merge = function(cell_num, compare, l, m, r) {
    var i; var j; var k;
    var n1 = m - l + 1;
    var n2 = r - m;
    var B; var E;
    
    for(i = 0; i < n1; i++) B[i] = rows[i].cells[cell_num];
    for(j = 0; j < n2; i++) E[i] = rows[i].cells[cell_num];
    
    i = 0; j = 0; k = 0;
    while(i < n1 && j < n2) {
        
    }
}

var swap = function(a, b) {
    var tmp = a;
    a = b;
    b = tmp;
}

// enums don't exist in js. These all correspond with cells[index] value
var fakeenum = function(cell_desc) {
    if(cell_desc == "name") {
        return 0;
    } else if(cell_desc == "interest") {
        return 2;
    } else if(cell_desc == "date") {
        return 5;
    }
}


if(order == "name") {
    rows.sort( (a, b) => {return a.cells[0]-b.cells[0]});
    document.getElementById("descriptions").innerHTML = "name";
} else if(order == "interest") {
    document.getElementById("descriptions").innerHTML = "interest";
} else if(order == "date") {
    document.getElementById("descriptions").innerHTML = "date";
} else {
    document.getElementById("descriptions").innerHTML = "failure";
}
