let memoria = [];
let stackPointer = -1;
let pc = 0;
let pcAnterior = 0;
let debugFlag = 0;
let step = false;
let statusBreakpoint = 0
let dev = false
let codigo = [];   
let tabela = {};  
let breakpoints = {};

if (!dev) {
  console.log = () => { }
  console.table = () => { }
}


function reset() {
  window.location.reload(true);
}

async function rodarCodigo() {
  let stackWindow = document.getElementById("stack");
  while (pc < codigo.length) {
    let line = codigo[pc]
    let elementos = line.trim().split(" ")
    let funcao = elementos.shift()
    let linhaAnterior = document.getElementById("line-" + pcAnterior);
    let linha = document.getElementById("line-" + pc)
    pcAnterior = pc;

    if (debugFlag == 1) {
      linhaAnterior.classList.remove("highlight");
      linha.classList.add("highlight");
      if (breakpoints[pc] == true) {
        statusBreakpoint = 1;
      }

      if (statusBreakpoint == 1) {
        if (step == false) {
          return;
        }
        else {
          step = false;
        }
      }
    }

    elementos.forEach((e, index, arr) => {
      if (e.length != 0) {
        if (e.match(/^[0-9]+$/) == null) {
          arr[index] = tabela[e];
        }
        else {
          arr[index] = +e;
        }
      }
    })

    if (!(funcao in tabela)) {
      if (funcao === "RD") {

        do {
          var answer = prompt("Digite o valor de INPUT: ")



          sleep = (ms) => {
            return new Promise(resolve => setTimeout(resolve, ms));
          }
          await sleep(0.5)

          if (answer === "true")
            answer = parseInt("1")
          else if (answer === "false")
            answer = parseInt("0")
          else
            answer = parseInt(answer)

        } while (isNaN(answer));

        if (!isNaN(answer)) {
          instrucoes["RD"](+answer)
        }
      }
      else {
        if (funcao === "HLT")
          return
        else {

          instrucoes[funcao](...elementos)
        }
      }
    }
    pc++;

    stackWindow.value += "PILHA: " + pc;
    stackWindow.value += "\r\n";
    
    stackWindow.scrollTop = stackWindow.scrollHeight;
  }
}


function openFile() {
  var input = document.createElement('input');
  input.type = 'file';

  input.onchange = e => {
    
    var file = e.target.files[0];

    
    var reader = new FileReader();
    reader.readAsText(file, 'UTF-8');

    
    reader.onload = readerEvent => {
      var content = readerEvent.target.result;
      montarTexto(content);
    }
  }
  input.click();
}

function montarTexto(code) {
  const lines = code.split("\n");                   
  div = document.querySelector(".code-window");     
  div.innerHTML = "";                               
  ol = document.createElement("ol")                 
  ol.classList.add("code-list");                    
  div.appendChild(ol)                               
  let numLinha = 1                                  
  lines.forEach((line, index, array) =>   {
    let clickou = false;

    
    if (line.includes('NULL')){
      tabela[line.split(' ')[0]] = numLinha - 1;
    }

    const li = document.createElement("li");       

    
    const divBreak = document.createElement("div")  
    divBreak.classList.add("break-div")             

    const divNumber = document.createElement("div") 
    divNumber.classList.add("number-div")           

    const divLine = document.createElement("div")   
    divLine.classList.add("line-div")               

    const breakButton = document.createElement("button");
    breakButton.setAttribute("id", "break-" + index);
    breakButton.innerHTML = "<i class='fas fa-circle select-trans'></i>";
    breakButton.addEventListener("click", function () {
      numLinha = this.id.split("-")[1];
      if (clickou === false) {
        breakpoints[numLinha] = true;
        breakButton.innerHTML = "<i class='fas fa-circle break-div'></i>"
        clickou = true;
      }
      else {
        breakpoints[numLinha] = false;
        breakButton.innerHTML = "<i class='fas fa-circle select-trans'></i>";
        clickou = false;
      }
    });
    divBreak.appendChild(breakButton);

    const numText = document.createTextNode(numLinha) 
    divNumber.appendChild(numText)                    

    
    const lineText = document.createTextNode(line)    
    divLine.appendChild(lineText)                     

    breakpoints[numLinha - 1] = false;                

    numLinha++;                                       

    li.appendChild(divBreak);
    li.appendChild(divNumber);                        
    li.appendChild(divLine);                          

    ol.appendChild(li);                               

    codigo.push(line);                                
  });
}

let junk;
let instrucoes = {
  "LDC": (k) => {
    stackPointer = stackPointer + 1
    memoria[stackPointer] = k
  },
  "LDV": (n) => {
    stackPointer = stackPointer + 1
    memoria[stackPointer] = memoria[n]
  },
  "ADD": () => {
    memoria[stackPointer - 1] = memoria[stackPointer - 1] + memoria[stackPointer]
    junk = memoria.pop()
    stackPointer = stackPointer - 1
  },
  "SUB": () => {
    memoria[stackPointer - 1] = memoria[stackPointer - 1] - memoria[stackPointer]
    junk = memoria.pop()
    stackPointer = stackPointer - 1
  },
  "MULT": () => {
    memoria[stackPointer - 1] = memoria[stackPointer - 1] * memoria[stackPointer]
    junk = memoria.pop()
    stackPointer = stackPointer - 1
  },
  "DIVI": () => {
    memoria[stackPointer - 1] = Math.trunc(memoria[stackPointer - 1] / memoria[stackPointer])
    junk = memoria.pop()
    stackPointer = stackPointer - 1
  },
  "INV": () => {
    memoria[stackPointer] = -memoria[stackPointer]
  },
  "AND": () => {
    if (memoria[stackPointer - 1] == 1 && memoria[stackPointer] == 1) {
      memoria[stackPointer - 1] = 1
    }
    else {
      memoria[stackPointer - 1] = 0
    }
    junk = memoria.pop()
    stackPointer = stackPointer - 1
  },
  "OR": () => {
    if (memoria[stackPointer - 1] == 1 || memoria[stackPointer] == 1) {
      memoria[stackPointer - 1] = 1
    }
    else {
      memoria[stackPointer - 1] = 0
    }
    junk = memoria.pop()
    stackPointer = stackPointer - 1
  },
  "NEG": () => {
    memoria[stackPointer] = 1 - memoria[stackPointer]
  },
  "CME": () => {
    if (memoria[stackPointer - 1] < memoria[stackPointer]) {
      memoria[stackPointer - 1] = 1
    }
    else {
      memoria[stackPointer - 1] = 0
    }
    junk = memoria.pop()
    stackPointer = stackPointer - 1
  },
  "CMA": () => {
    if (memoria[stackPointer - 1] > memoria[stackPointer]) {
      memoria[stackPointer - 1] = 1
    }
    else {
      memoria[stackPointer - 1] = 0
    }
    junk = memoria.pop()
    stackPointer = stackPointer - 1
  },
  "CEQ": () => {
    if (memoria[stackPointer - 1] == memoria[stackPointer]) {
      memoria[stackPointer - 1] = 1
    }
    else {
      memoria[stackPointer - 1] = 0
    }
    junk = memoria.pop()
    stackPointer = stackPointer - 1
  },
  "CDIF": () => {
    if (memoria[stackPointer - 1] != memoria[stackPointer]) {
    }
    else {
      memoria[stackPointer - 1] = 0
    }
    junk = memoria.pop()
    stackPointer = stackPointer - 1
  },
  "CMEQ": () => {
    if (memoria[stackPointer - 1] <= memoria[stackPointer]) {
      memoria[stackPointer - 1] = 1
    }
    else {
      memoria[stackPointer - 1] = 0
    }
    junk = memoria.pop()
    stackPointer = stackPointer - 1
  },
  "CMAQ": () => {
    if (memoria[stackPointer - 1] >= memoria[stackPointer]) {
      memoria[stackPointer - 1] = 1
    }
    else {
      memoria[stackPointer - 1] = 0
    }
    junk = memoria.pop()
    stackPointer = stackPointer - 1
  },
  "START": () => {
    stackPointer = -1;
  },
  "HLT": () => {

  },
  "STR": (n) => {
    memoria[n] = memoria[stackPointer]
    junk = memoria.pop()
    stackPointer = stackPointer - 1
  },
  "JMP": (t) => {
    pc = t
  },
  "JMPF": (t) => {
    if (memoria[stackPointer] == 0) {
      pc = t
    }
    else {
      pc = pc
    }
    junk = memoria.pop()
    stackPointer = stackPointer - 1
  },
  "NULL": () => {
    return;
  },
  "RD": (value) => {
    stackPointer = stackPointer + 1
    memoria[stackPointer] = value
  },
  "PRN": () => {
    let out = '';
    out += memoria[stackPointer];
    out += "\r\n";
    document.getElementById("output").value += out
    document.getElementById("output").scrollTop = out.scrollHeight;
    junk = memoria.pop()
    stackPointer = stackPointer - 1
  },
  "ALLOC": (m, n) => {
    for (let k = 0; k < n; k++) {
      stackPointer = stackPointer + 1
      memoria[stackPointer] = memoria[m + k]
    }
  },
  "DALLOC": (m, n) => {
    for (let k = n - 1; k >= 0; k--) {
      memoria[m + k] = memoria[stackPointer]
      junk = memoria.pop()
      stackPointer = stackPointer - 1
    }
  },
  "CALL": (t, l) => {
    stackPointer = stackPointer + 1
    memoria[stackPointer] = pc + 1
    pc = l
  },
  "RETURN": () => {
    pc = memoria[stackPointer] - 1
    junk = memoria.pop()
    stackPointer = stackPointer - 1
  },
  "RETURNF": (m, n) => {
    topoPilha = memoria[stackPointer]
    junk = memoria.pop()
    stackPointer = stackPointer - 1

   
    for (let k = n - 1; k >= 0; k--) {
      memoria[m + k] = memoria[stackPointer]
      junk = memoria.pop()
      stackPointer = stackPointer - 1
    }
    pc = memoria[stackPointer] - 1
    junk = memoria.pop()
    stackPointer = stackPointer - 1
    stackPointer = stackPointer + 1
    memoria[stackPointer] = topoPilha
  },
};