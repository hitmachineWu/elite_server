// 自动关闭提示信息
document.addEventListener('DOMContentLoaded', function() {
    // 获取所有警告消息
    const alerts = document.querySelectorAll('.alert');
    
    // 为每个警告设置自动关闭
    alerts.forEach(alert => {
        // 5秒后自动关闭
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // 为模型卡片添加鼠标悬停效果
    const modelCards = document.querySelectorAll('.model-card');
    modelCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('shadow-lg');
        });
        card.addEventListener('mouseleave', function() {
            this.classList.remove('shadow-lg');
        });
    });
});