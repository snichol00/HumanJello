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
var merge_sorth, merge_sort, merge, studentInterests, arrToHtml, htmlToArr;
var arrToInterests, libero, protean, swap, fakeenum;
var order = document.getElementById("order").value;
var table = document.getElementsByTagName("table")[0];
var rows = document.getElementsByTagName("table")[0].rows;
var arr_rows = Array.from(table.rows);

var studentInterests = function(user_interests) {
    var student_interests = "events,academic,business,community_service,leadership,museums,nature,stem,humanities,scholarships".split(",");
    console.log(student_interests);
    var ans = [];
    for(var i = 0; i < student_interests.length; i++)
        if(user_interests[i] == "1")
            ans.push(student_interests[i]);
    return ans;
};

var user_interests = studentInterests(document.getElementById("user_interests")
                                      .innerText.slice(1, -1).split(", "));


var merge_sorth = function(cell_num, compare) {
    //l starts at one because row 0 is header
    merge_sort(cell_num, compare, 1, rows.length);
};

var merge_sort = function(cell_num, compare, l, r) {
    if(l < r) {
        var m = (l + r) / 2;
        merge_sort(cell_num, compare, l, m);
        merge_sort(cell_num, compare, m, r);
        merge(cell_num, compare, l, m, r);
    }
};

var merge = function(cell_num, compare, l, m, r) {
    var i; var j; var k;
    var n1 = m - l + 1;
    var n2 = r - m;
    var B; var E;

    for(i = 0; i < n1; i++) B[i] = rows[i].cells[cell_num];
    for(j = 0; j < n2; i++) E[i] = rows[i].cells[cell_num];

    i = 0; j = 0; k = 0;
    while(i < n1 && j < n2) {
        if(compare(B[i].innerText, E[j].innerText)) {
            rows[k].cells[cell_num].innerText = B[i].innerText;
            k++; i++;
        } else {
            rows[k].cells[cell_num].innerText = E[j].innerText;
            k++; j++;
        }
    }

    if(j < n1) {
        for(; i < n1; i++) {
            rows[k].cells[cell_num].innerText = B[i].innerText;
            k++;
        }
    } else {
        for(; j < n2; j++) {
            rows[k].cells[cell_num].innerText = E[j].innerText;
            k++;
        }
    }
};

// var arrToInterests = function() {
//     var ans = [];
//     for(var i = 0; i < rows.length; i++) {
//         var j;
//         for(j in rows[i].cells[fakeenum("interest")].innerText.split(" ")) {
//             if(i == ans.length) {
//                 if(user_interests.indexOf(j) > 0) ans.push(1);
//                 else ans.push(0);
//             } else {
//                 if(user_interests.indexOf(j) > 0) ans[-1]++;
//             }
//         }
//     }
// }

var arrToHtml = function(cells_num, arr) {
    for(var i = 0; i < arr.length; i++) {
        console.log(`${i}: ${arr[i].innerHTML}`)
        rows[i + 1].cells[cells_num].innerHTML = arr[i].innerHTML;
    }
};

var htmlToArr = function(cells_num) {
    var ans = [];
    for(var i = 1; i < rows.length; i++) {
        //ans.push(rows[i].cells[cells_num].innerText);
        ans.push(rows[i].cells[cells_num]);
    }
    return ans;
};

var stringToInterests = function(interests) {
    return interests.innerText.slice(1, -1).split(", ")
}

var getNumInterests = function(a) {
    var ans = 0;
    for(var i = 0; i < stringToInterests(a).length; i++) {
        if(user_interests.indexOf(stringToInterests(a)[i]) > 0) ans++;
    }
    return ans;
}

// enums don't exist in js. These all correspond with cells[index] value
var fakeenum = function(cell_desc) {
    if(cell_desc == "name") {
        return 0;
    } else if(cell_desc == "interest") {
        return 2;
    } else if(cell_desc == "date") {
        return 5;
    } else {
        return -1;
    }
};

var protean = function() {
    console.log("Kecleon");
    order = document.getElementById("order").value;
    if(order == "name") {
        var sorted_arr = htmlToArr(fakeenum("name")).sort(
            (a, b) => {return a.innerText > b.innerText;}
        );
        arrToHtml(fakeenum("name"), sorted_arr);
    } else if(order == "interest") {
        var htmlElements = htmlToArr(fakeenum("interest")).sort(
            (a, b) => {
                getNumInterests(a) > getNumInterests(b);
            }
        );
        arrToHtml(htmlElements, htmlElements);
    } else if(order == "date") {
        var sorted_arr = htmlToArr(fakeenum("date")).sort(
            (a, b) => {return a.innerText > b.innerText;}
        );
        arrToHtml(fakeenum("date"), sorted_arr);
    } else {
        document.getElementById("descriptions").innerText = "Error";
    }
};

// var libero = function() {
//     if(order == "name") {
//         merge_sorth(
//             fakeenum("name"),
//             (a, b) => {
//                 return a.innerText > b.innerText;
//             }
//         );
//     } else if(order == "interest") {
//         merge_sorth(
//             fakeenum("interest"),
//             (a, b) => {
//                 var user_interests = studentInterests(user_interests).slice(1, -1).split(", ");
//                 studentInterests(user_interests);
//             }
//         );
//     }
// };

// var swap = function(a, b) {
//     var tmp = a;
//     a = b;
//     b = tmp;
// };

// document.getElementById("order").addEventListener("change", libero);
document.getElementById("order").addEventListener("change", protean);

// if(order == "name") {
//     rows.sort( (a, b) => {return a.cells[0]-b.cells[0];});
//     document.getElementById("descriptions").innerHTML = "name";
// } else if(order == "interest") {
//     document.getElementById("descriptions").innerHTML = "interest";
// } else if(order == "date") {
//     document.getElementById("descriptions").innerHTML = "date";
// } else {
//     document.getElementById("descriptions").innerHTML = "failure";
// }
