document.addEventListener('DOMContentLoaded', function() {
    // 收藏按钮功能
    const favoriteButtons = document.querySelectorAll('.btn-favorite');
    
    favoriteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const agentId = this.getAttribute('data-agent-id');
            
            fetch(`/api/toggle-favorite/${agentId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'added') {
                    this.classList.add('active');
                    this.innerHTML = '<span class="icon">★</span> 取消收藏';
                } else {
                    this.classList.remove('active');
                    this.innerHTML = '<span class="icon">☆</span> 收藏';
                    
                    // 如果在收藏页面，移除卡片
                    if (window.location.pathname.includes('/favorites')) {
                        const card = this.closest('.agent-card');
                        card.style.opacity = '0';
                        setTimeout(() => {
                            card.remove();
                            
                            // 检查是否还有卡片
                            const remainingCards = document.querySelectorAll('.agent-card');
                            if (remainingCards.length === 0) {
                                const container = document.querySelector('.agents-grid');
                                container.innerHTML = `
                                    <div class="empty-state">
                                        <div class="empty-icon">⭐</div>
                                        <h3>暂无收藏</h3>
                                        <p>您还没有收藏任何智能体，可以在"课程智能体"页面找到并收藏感兴趣的智能体。</p>
                                        <a href="/dashboard/agents" class="btn btn-primary">浏览智能体</a>
                                    </div>
                                `;
                            }
                        }, 300);
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });

    // 调整iframe高度以适应窗口大小
    function adjustIframeHeight() {
        const iframe = document.querySelector('.embed-container iframe');
        if (iframe) {
            const headerHeight = document.querySelector('.page-header').offsetHeight;
            const windowHeight = window.innerHeight;
            const padding = 60; // 考虑页面内边距
            iframe.style.height = `${windowHeight - headerHeight - padding}px`;
        }
    }

    // 页面加载和窗口大小改变时调整iframe高度
    if (document.querySelector('.embed-container')) {
        adjustIframeHeight();
        window.addEventListener('resize', adjustIframeHeight);
    }
});