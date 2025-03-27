let resultadoFaturamento = 0;
let aliquota = 0;


// ANEXO III

if( resultadoFaturamento <= 180000){
    aliquota = (6/100)
}else if(resultadoFaturamento <= 360000){
    aliquota = (112/100)
}else if(resultadoFaturamento <= 720000){
    aliquota = (135/100)
}else if(resultadoFaturamento <= 1800000){
    aliquota = (16/100)
}else if(resultadoFaturamento <= 3600000){
    aliquota = (21/100)
}else if (resultadoFaturamento<= 4800000){
    aliquota = (33/100)
}

// Refatore em cópia este código para uma condicional de excel, sendo o resultadoFaturamento informações contidas na coluna L, aliquota sendo uma informação contida em outra aba de excel na coluna D


//Alíquota
// =SE(L{posição}<=180000; 'ANEXOS '!D31; 
//     SE(L{posição}<=360000; 'ANEXOS '!D32;
//     SE(L{posição}<=720000; 'ANEXOS '!D33;
//     SE(L{posição}<=1800000; 'ANEXOS '!D34;
//     SE(L{posição}<=3600000; 'ANEXOS '!D35;
//     SE(L{posição}<=4800000; 'ANEXOS '!D36; ""))))))
    

// VALOR A DEDUZIR
// =SE(L{posição}<=180000; 'ANEXOS '!E{posiçãoDedução}; 
//     SE(L{posição}<=360000; 'ANEXOS '!E{posiçãoDedução};
//     SE(L{posição}<=720000; 'ANEXOS '!E{posiçãoDedução};
//     SE(L{posição}<=1800000; 'ANEXOS '!E{posiçãoDedução};
//     SE(L{posição}<=3600000; 'ANEXOS '!E{posiçãoDedução};
//     SE(L{posição}<=4800000; 'ANEXOS '!E{posiçãoDedução}; ""))))))
  
// CALCULO ISS


// CALCULO ALIQUOTA EFETIVA
