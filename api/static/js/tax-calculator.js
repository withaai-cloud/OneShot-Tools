// SA Tax Split Optimizer Calculator

// 2024/2025 SA Individual Tax Brackets
function calculateIndividualTax(income) {
    if (income <= 237100) return 0;
    if (income <= 370500) return (income - 237100) * 0.18;
    if (income <= 512800) return 24012 + (income - 370500) * 0.26;
    if (income <= 673000) return 61010 + (income - 512800) * 0.31;
    if (income <= 857900) return 110672 + (income - 673000) * 0.36;
    if (income <= 1817000) return 177236 + (income - 857900) * 0.39;
    return 551196 + (income - 1817000) * 0.45;
}

// SBC Tax Brackets (0% up to R95,750, then graduated rates)
function calculateSBCTax(income) {
    if (income <= 95750) return 0;
    if (income <= 365000) return (income - 95750) * 0.07;
    if (income <= 550000) return 18847.50 + (income - 365000) * 0.21;
    return 57697.50 + (income - 550000) * 0.27;
}

function formatCurrency(amount) {
    return 'R ' + amount.toLocaleString('en-ZA', {minimumFractionDigits: 2, maximumFractionDigits: 2});
}

function calculateOptimalSplit() {
    const totalIncome = parseFloat(document.getElementById('totalIncome').value);
    
    if (!totalIncome || totalIncome <= 0) {
        alert('Please enter a valid income amount');
        return;
    }
    
    let optimalIndividual = 0;
    let optimalSBC = totalIncome;
    let minTotalTax = calculateIndividualTax(0) + calculateSBCTax(totalIncome);
    
    // Try different splits in increments
    const increment = 1000;
    for (let individualAmount = 0; individualAmount <= totalIncome; individualAmount += increment) {
        const sbcAmount = totalIncome - individualAmount;
        const individualTax = calculateIndividualTax(individualAmount);
        const sbcTax = calculateSBCTax(sbcAmount);
        const totalTax = individualTax + sbcTax;
        
        if (totalTax < minTotalTax) {
            minTotalTax = totalTax;
            optimalIndividual = individualAmount;
            optimalSBC = sbcAmount;
        }
    }
    
    // Fine-tune around the optimal point
    const searchRange = increment * 2;
    for (let individualAmount = Math.max(0, optimalIndividual - searchRange); 
         individualAmount <= Math.min(totalIncome, optimalIndividual + searchRange); 
         individualAmount += 100) {
        const sbcAmount = totalIncome - individualAmount;
        const individualTax = calculateIndividualTax(individualAmount);
        const sbcTax = calculateSBCTax(sbcAmount);
        const totalTax = individualTax + sbcTax;
        
        if (totalTax < minTotalTax) {
            minTotalTax = totalTax;
            optimalIndividual = individualAmount;
            optimalSBC = sbcAmount;
        }
    }
    
    const optimalIndividualTax = calculateIndividualTax(optimalIndividual);
    const optimalSBCTax = calculateSBCTax(optimalSBC);
    const totalTax = optimalIndividualTax + optimalSBCTax;
    const effectiveRate = (totalTax / totalIncome) * 100;
    
    // Calculate tax if all income was individual or all SBC
    const allIndividualTax = calculateIndividualTax(totalIncome);
    const allSBCTax = calculateSBCTax(totalIncome);
    const savingsVsIndividual = allIndividualTax - totalTax;
    const savingsVsSBC = allSBCTax - totalTax;
    
    // Display results
    document.getElementById('individualIncome').textContent = formatCurrency(optimalIndividual);
    document.getElementById('individualTax').textContent = formatCurrency(optimalIndividualTax);
    document.getElementById('sbcIncome').textContent = formatCurrency(optimalSBC);
    document.getElementById('sbcTax').textContent = formatCurrency(optimalSBCTax);
    document.getElementById('totalTax').textContent = formatCurrency(totalTax);
    document.getElementById('effectiveRate').textContent = effectiveRate.toFixed(2) + '%';
    
    // Display savings
    document.getElementById('savingsIndividual').textContent = formatCurrency(savingsVsIndividual);
    document.getElementById('savingsSBC').textContent = formatCurrency(savingsVsSBC);
    
    document.getElementById('results').classList.remove('hidden');
}

// Allow Enter key to calculate
document.getElementById('totalIncome').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        calculateOptimalSplit();
    }
});
