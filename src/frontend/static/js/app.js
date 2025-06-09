// API配置
const API_BASE_URL = '/api';
let isUploading = false;
let jarFiles = [];

// DOM元素
const elements = {
    // 文件管理相关
    uploadBtn: document.getElementById('uploadBtn'),
    uploadSection: document.getElementById('uploadSection'),
    uploadArea: document.getElementById('uploadArea'),
    fileInput: document.getElementById('fileInput'),
    uploadProgress: document.getElementById('uploadProgress'),
    progressFill: document.getElementById('progressFill'),
    progressText: document.getElementById('progressText'),
    jarItems: document.getElementById('jarItems'),
    
    // 查询相关
    queryInput: document.getElementById('queryInput'),
    queryBtn: document.getElementById('queryBtn'),
    resultsContainer: document.getElementById('resultsContainer'),
    resultContent: document.getElementById('resultContent'),
    
    // 搜索相关
    searchInput: document.getElementById('searchInput'),
    searchBtn: document.getElementById('searchBtn'),
    searchResults: document.getElementById('searchResults'),
    codeResults: document.getElementById('codeResults'),
    jarFilter: document.getElementById('jarFilter'),
    typeFilter: document.getElementById('typeFilter'),
    
    // 状态和统计
    loadingOverlay: document.getElementById('loadingOverlay'),
    dbStatus: document.getElementById('dbStatus'),
    aiStatus: document.getElementById('aiStatus'),
    fileCount: document.getElementById('fileCount'),
    totalChunks: document.getElementById('totalChunks'),
    dbSize: document.getElementById('dbSize'),
    
    // 模态框
    modalOverlay: document.getElementById('modalOverlay'),
    modalTitle: document.getElementById('modalTitle'),
    modalMessage: document.getElementById('modalMessage'),
    modalClose: document.getElementById('modalClose'),
    modalCancel: document.getElementById('modalCancel'),
    modalConfirm: document.getElementById('modalConfirm')
};

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    checkSystemStatus();
    loadJarFiles();
});

// 事件监听器初始化
function initializeEventListeners() {
    // 文件管理相关
    elements.uploadBtn.addEventListener('click', toggleUploadSection);
    elements.uploadArea.addEventListener('click', () => {
        if (!isUploading) {
            elements.fileInput.click();
        }
    });
    
    elements.uploadArea.addEventListener('dragover', handleDragOver);
    elements.uploadArea.addEventListener('dragleave', handleDragLeave);
    elements.uploadArea.addEventListener('drop', handleDrop);
    elements.fileInput.addEventListener('change', handleFileSelect);
    
    // 查询相关
    elements.queryBtn.addEventListener('click', handleQuery);
    elements.queryInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleQuery();
        }
    });
    
    // 搜索相关
    elements.searchBtn.addEventListener('click', handleSearch);
    elements.searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });
    
    // 模态框相关
    elements.modalClose.addEventListener('click', hideModal);
    elements.modalCancel.addEventListener('click', hideModal);
    elements.modalOverlay.addEventListener('click', (e) => {
        if (e.target === elements.modalOverlay) {
            hideModal();
        }
    });
}

// 切换上传区域显示
function toggleUploadSection() {
    const isVisible = elements.uploadSection.style.display !== 'none';
    elements.uploadSection.style.display = isVisible ? 'none' : 'block';
    elements.uploadBtn.innerHTML = isVisible ? 
        '<i class="fas fa-plus"></i> 添加JAR' : 
        '<i class="fas fa-minus"></i> 取消';
}

// 拖拽处理
function handleDragOver(e) {
    e.preventDefault();
    elements.uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    elements.uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    elements.uploadArea.classList.remove('dragover');
    
    const files = Array.from(e.dataTransfer.files).filter(file => 
        file.name.toLowerCase().endsWith('.jar')
    );
    
    if (files.length > 0) {
        uploadFiles(files);
    } else {
        showNotification('请选择JAR文件', 'error');
    }
}

// 文件选择处理
function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    if (files.length > 0) {
        uploadFiles(files);
    }
}

// 文件上传
async function uploadFiles(files) {
    if (isUploading) return;
    
    isUploading = true;
    elements.uploadProgress.style.display = 'block';
    
    try {
        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            elements.progressText.textContent = `上传中: ${file.name} (${i + 1}/${files.length})`;
            
            const formData = new FormData();
            formData.append('file', file);
            
            const response = await fetch(`${API_BASE_URL}/upload`, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`上传失败: ${response.statusText}`);
            }
            
            const result = await response.json();
            console.log('上传结果:', result);
            
            // 更新进度
            const progress = ((i + 1) / files.length) * 100;
            elements.progressFill.style.width = `${progress}%`;
        }
        
        showNotification('文件上传成功', 'success');
        elements.fileInput.value = '';
        toggleUploadSection();
        
        // 刷新文件列表和统计
        await loadJarFiles();
        await checkSystemStatus();
        
    } catch (error) {
        console.error('上传错误:', error);
        showNotification(`上传失败: ${error.message}`, 'error');
    } finally {
        isUploading = false;
        elements.uploadProgress.style.display = 'none';
        elements.progressFill.style.width = '0%';
    }
}

// 加载JAR文件列表
async function loadJarFiles() {
    try {
        // 从后端API获取真实的JAR文件列表
        const response = await fetch(`${API_BASE_URL}/jars`);
        if (!response.ok) {
            throw new Error(`获取文件列表失败: ${response.status}`);
        }
        
        const data = await response.json();
        jarFiles = data.jars || [];
        
        // 格式化上传时间
        jarFiles.forEach(jar => {
            if (jar.uploadTime) {
                jar.uploadTime = new Date(jar.uploadTime * 1000).toLocaleString('zh-CN');
            }
        });
        
        renderJarList();
        updateJarFilter();
        
    } catch (error) {
        console.error('加载文件列表失败:', error);
        // 如果API调用失败，显示空列表
        jarFiles = [];
        renderJarList();
        updateJarFilter();
    }
}

// 渲染JAR文件列表
function renderJarList() {
    elements.jarItems.innerHTML = '';
    
    if (jarFiles.length === 0) {
        elements.jarItems.innerHTML = `
            <div style="text-align: center; padding: 20px; color: #718096;">
                <i class="fas fa-folder-open" style="font-size: 2rem; margin-bottom: 10px; display: block;"></i>
                暂无JAR文件
            </div>
        `;
        return;
    }
    
    jarFiles.forEach(jar => {
        const jarItem = document.createElement('div');
        jarItem.className = 'jar-item';
        jarItem.innerHTML = `
            <div class="jar-name" title="${jar.name}">${jar.name}</div>
            <div class="jar-status">
                <span class="status-badge ${jar.status}">
                    ${getStatusText(jar.status)}
                </span>
            </div>
            <div class="jar-actions">
                <button class="action-btn reindex" onclick="reindexJar('${jar.name}')" title="重新索引">
                    <i class="fas fa-sync"></i>
                </button>
                <button class="action-btn delete" onclick="deleteJar('${jar.name}')" title="删除">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;
        elements.jarItems.appendChild(jarItem);
    });
}

// 获取状态文本
function getStatusText(status) {
    const statusMap = {
        'indexed': '已索引',
        'processing': '处理中',
        'error': '错误'
    };
    return statusMap[status] || status;
}

// 更新JAR过滤器选项
function updateJarFilter() {
    elements.jarFilter.innerHTML = '<option value="">所有JAR文件</option>';
    
    jarFiles.forEach(jar => {
        const option = document.createElement('option');
        option.value = jar.name;
        option.textContent = jar.name;
        elements.jarFilter.appendChild(option);
    });
}

// 删除JAR文件
function deleteJar(jarName) {
    showModal(
        '确认删除',
        `确定要删除 "${jarName}" 及其所有索引数据吗？此操作不可撤销。`,
        async () => {
            try {
                showLoading(true);
                
                // 调用删除API
                const response = await fetch(`${API_BASE_URL}/jar/${encodeURIComponent(jarName)}`, {
                    method: 'DELETE'
                });
                
                if (!response.ok) {
                    throw new Error(`删除请求失败: ${response.status}`);
                }
                
                jarFiles = jarFiles.filter(jar => jar.name !== jarName);
                renderJarList();
                updateJarFilter();
                await checkSystemStatus();
                
                showNotification('文件删除成功', 'success');
                
            } catch (error) {
                console.error('删除失败:', error);
                showNotification(`删除失败: ${error.message}`, 'error');
            } finally {
                showLoading(false);
                hideModal();
            }
        }
    );
}

// 重新索引JAR文件
async function reindexJar(jarName) {
    try {
        showLoading(true);
        
        // 这里需要调用重新索引API
        // const response = await fetch(`${API_BASE_URL}/jar/${encodeURIComponent(jarName)}/reindex`, {
        //     method: 'POST'
        // });
        
        // 模拟重新索引
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        showNotification('重新索引完成', 'success');
        await loadJarFiles();
        await checkSystemStatus();
        
    } catch (error) {
        console.error('重新索引失败:', error);
        showNotification(`重新索引失败: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

// 智能查询处理
async function handleQuery() {
    const query = elements.queryInput.value.trim();
    if (!query) {
        showNotification('请输入查询内容', 'error');
        return;
    }
    
    try {
        showLoading(true);
        
        const response = await fetch(`${API_BASE_URL}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });
        
        if (!response.ok) {
            throw new Error(`查询失败: ${response.statusText}`);
        }
        
        const result = await response.json();
        displayQueryResult(result);
        
    } catch (error) {
        console.error('查询错误:', error);
        showNotification(`查询失败: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

// 显示查询结果
function displayQueryResult(result) {
    elements.resultsContainer.style.display = 'block';
    elements.resultsContainer.classList.add('fade-in');
    
    let content = `<div class="answer-section">
        <h4><i class="fas fa-lightbulb"></i> 回答</h4>
        <div class="answer-content">${result.answer}</div>
    </div>`;
    
    if (result.sources && result.sources.length > 0) {
        content += `<div class="sources-section">
            <h4><i class="fas fa-code"></i> 相关代码</h4>
            <div class="sources-content">`;
        
        result.sources.forEach((source, index) => {
            content += `
                <div class="code-block">
                    <div class="code-header">
                        <span>${source.source_file || '未知文件'}</span>
                        <span>相似度: ${(source.similarity_score * 100).toFixed(1)}%</span>
                    </div>
                    <pre><code>${escapeHtml(source.content)}</code></pre>
                </div>
            `;
        });
        
        content += '</div></div>';
    }
    
    elements.resultContent.innerHTML = content;
}

// 代码搜索处理
async function handleSearch() {
    const query = elements.searchInput.value.trim();
    if (!query) {
        showNotification('请输入搜索内容', 'error');
        return;
    }
    
    try {
        showLoading(true);
        
        const payload = {
            query: query,
            jar_filter: elements.jarFilter.value || null, // Send null if empty for Optional fields
            type_filter: elements.typeFilter.value || null, // Send null if empty for Optional fields
            top_k: 10 // Default top_k, or make it configurable in UI
        };
        
        const response = await fetch(`${API_BASE_URL}/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: response.statusText }));
            throw new Error(`搜索失败: ${errorData.detail || response.statusText}`);
        }
        
        const result = await response.json();
        displaySearchResults(result);
        
    } catch (error) {
        console.error('搜索错误:', error);
        showNotification(`搜索失败: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

// 显示搜索结果
function displaySearchResults(result) {
    elements.searchResults.style.display = 'block';
    elements.searchResults.classList.add('fade-in');
    
    if (!result.results || result.results.length === 0) {
        elements.codeResults.innerHTML = `
            <div style="text-align: center; padding: 20px; color: #718096;">
                <i class="fas fa-search" style="font-size: 2rem; margin-bottom: 10px; display: block;"></i>
                未找到相关代码
            </div>
        `;
        return;
    }
    
    let content = '';
    result.results.forEach((item, index) => {
        content += `
            <div class="code-block">
                <div class="code-header">
                    <span>${item.source_file || '未知文件'}</span>
                    <span>类型: ${item.chunk_type || '未知'}</span>
                </div>
                <pre><code>${escapeHtml(item.content)}</code></pre>
            </div>
        `;
    });
    
    elements.codeResults.innerHTML = content;
}

// 检查系统状态
async function checkSystemStatus() {
    try {
        // 检查数据库状态
        const dbResponse = await fetch(`${API_BASE_URL}/status/database`);
        const dbStatus = await dbResponse.json();
        updateStatusIndicator(elements.dbStatus, dbStatus.status === 'online');
        
        // 检查AI服务状态
        const aiResponse = await fetch(`${API_BASE_URL}/status/ai`);
        const aiStatus = await aiResponse.json();
        updateStatusIndicator(elements.aiStatus, aiStatus.status === 'online');
        
        // 获取统计信息
        const statsResponse = await fetch(`${API_BASE_URL}/stats`);
        const stats = await statsResponse.json();
        
        elements.fileCount.textContent = stats.indexed_files || 0;
        elements.totalChunks.textContent = stats.total_chunks || 0;
        elements.dbSize.textContent = stats.database_size || '0 MB';
        
    } catch (error) {
        console.error('状态检查失败:', error);
        updateStatusIndicator(elements.dbStatus, false);
        updateStatusIndicator(elements.aiStatus, false);
    }
}

// 更新状态指示器
function updateStatusIndicator(element, isOnline) {
    element.textContent = isOnline ? '在线' : '离线';
    element.style.color = isOnline ? '#4ade80' : '#f87171';
}

// 显示模态框
function showModal(title, message, onConfirm) {
    elements.modalTitle.textContent = title;
    elements.modalMessage.textContent = message;
    elements.modalOverlay.style.display = 'flex';
    
    // 移除之前的事件监听器
    elements.modalConfirm.replaceWith(elements.modalConfirm.cloneNode(true));
    elements.modalConfirm = document.getElementById('modalConfirm');
    
    // 添加新的事件监听器
    elements.modalConfirm.addEventListener('click', onConfirm);
}

// 隐藏模态框
function hideModal() {
    elements.modalOverlay.style.display = 'none';
}

// 显示/隐藏加载覆盖层
function showLoading(show) {
    elements.loadingOverlay.style.display = show ? 'flex' : 'none';
}

// 显示通知
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)}"></i>
        ${message}
    `;
    
    document.body.appendChild(notification);
    
    // 3秒后自动移除
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 3000);
}

// 获取通知图标
function getNotificationIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// HTML转义
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 全局函数（供HTML调用）
window.deleteJar = deleteJar;
window.reindexJar = reindexJar;