function sumUP(b){
    var res = b.map(b => b.pendingAmount).reduce((acc, b) => b + acc);
    return res
}
