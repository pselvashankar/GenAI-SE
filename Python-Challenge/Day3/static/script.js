class CalculatorApp {
    constructor() {
        this.history = [];
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        document.getElementById('calculateBtn').addEventListener('click', () => this.calculate());
        document.getElementById('clearBtn').addEventListener('click', () => this.clearAll());
        
        // Enter key support
        document.getElementById('num1').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.calculate();
        });
        
        document.getElementById('num2').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.calculate();
        });
        
        // Operation change
        document.getElementById('operation').addEventListener('change', () => {
            this.updateOperationDisplay();
        });
    }

    async calculate() {
        const num1 = document.getElementById('num1').value;
        const num2 = document.getElementById('num2').value;
        const operation = document.getElementById('operation').value;

        // Basic validation
        if (!num1 || !num2) {
            this.showError('Please enter both numbers');
            return;
        }

        // Show loading
        this.showLoading();

        try {
            const response = await fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    num1: num1,
                    num2: num2,
                    operation: operation
                })
            });

            const data = await response.json();

            if (data.success) {
                this.showSuccess(data);
                this.addToHistory(data);
            } else {
                this.showError(data.error);
            }

        } catch (error) {
            this.showError('Network error: Could not connect to server');
            console.error('Error:', error);
        }
    }

    showLoading() {
        const resultDisplay = document.getElementById('resultDisplay');
        const detailedResult = document.getElementById('detailedResult');
        
        resultDisplay.innerHTML = `
            <div class="result-placeholder">
                <i class="fas fa-spinner fa-spin"></i>
                <p>Calculating...</p>
            </div>
        `;
        resultDisplay.className = 'result-display';
        detailedResult.innerHTML = '';
    }

    showSuccess(data) {
        const resultDisplay = document.getElementById('resultDisplay');
        const detailedResult = document.getElementById('detailedResult');
        
        resultDisplay.innerHTML = `
            <div class="fade-in">
                <div class="result-main">
                    <i class="fas fa-check-circle"></i> Result: ${data.result}
                </div>
            </div>
        `;
        resultDisplay.className = 'result-display result-success fade-in';
        
        detailedResult.innerHTML = `
            <div class="fade-in">
                <strong><i class="fas fa-calculator"></i> Calculation:</strong> ${data.full_calculation}
            </div>
        `;
    }

    showError(message) {
        const resultDisplay = document.getElementById('resultDisplay');
        const detailedResult = document.getElementById('detailedResult');
        
        resultDisplay.innerHTML = `
            <div class="fade-in">
                <div class="result-main">
                    <i class="fas fa-exclamation-triangle"></i> Error
                </div>
                <div>${message}</div>
            </div>
        `;
        resultDisplay.className = 'result-display result-error fade-in';
        detailedResult.innerHTML = '';
    }

    addToHistory(data) {
        this.history.unshift({
            expression: data.expression,
            result: data.result,
            timestamp: new Date().toLocaleTimeString()
        });

        // Keep only last 10 calculations
        if (this.history.length > 10) {
            this.history.pop();
        }

        this.updateHistoryDisplay();
    }

    updateHistoryDisplay() {
        const historyList = document.getElementById('historyList');
        
        if (this.history.length === 0) {
            historyList.innerHTML = '<div class="history-empty">No calculations yet</div>';
            return;
        }

        historyList.innerHTML = this.history.map(item => `
            <div class="history-item fade-in">
                <strong>${item.expression} = ${item.result}</strong>
                <div style="font-size: 0.8em; color: #7f8c8d;">${item.timestamp}</div>
            </div>
        `).join('');
    }

    clearAll() {
        document.getElementById('num1').value = '';
        document.getElementById('num2').value = '';
        document.getElementById('operation').value = 'add';
        
        const resultDisplay = document.getElementById('resultDisplay');
        const detailedResult = document.getElementById('detailedResult');
        
        resultDisplay.innerHTML = `
            <div class="result-placeholder">
                <i class="fas fa-clock"></i>
                <p>Waiting for calculation...</p>
            </div>
        `;
        resultDisplay.className = 'result-display';
        detailedResult.innerHTML = '';
        
        document.getElementById('num1').focus();
    }

    updateOperationDisplay() {
        // You can add dynamic operation symbol updates here if needed
    }
}

// Initialize the calculator when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new CalculatorApp();
});