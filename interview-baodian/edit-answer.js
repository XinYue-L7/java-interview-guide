/**
 * 面试宝典 · 答案编辑系统
 * - 编辑模式开关
 * - 点击答案区域直接编辑
 * - 修改自动保存到 localStorage
 * - 支持导出/导入修改
 */
(function () {
  const SECTION = document.body.dataset.section;

  // —— 注入编辑系统 CSS ——
  const style = document.createElement('style');
  style.textContent = `
    .edit-toolbar {
      display: flex; gap: 8px; align-items: center;
      margin-top: 8px; flex-wrap: wrap;
    }
    .edit-mode-btn {
      font-size: 12px; padding: 5px 14px;
      border: 1px solid #888; background: transparent; color: #888;
      border-radius: 16px; cursor: pointer; transition: all .2s;
    }
    .edit-mode-btn:hover { border-color: #c9a96e; color: #c9a96e; }
    .edit-mode-btn.active {
      background: #c9a96e; color: #fff; border-color: #c9a96e;
    }
    .export-btn {
      font-size: 12px; padding: 5px 14px;
      border: 1px dashed #ccc; background: transparent; color: #999;
      border-radius: 16px; cursor: pointer; transition: all .2s;
    }
    .export-btn:hover { border-color: #555; color: #555; }
    .edit-mode-btn.active ~ .export-btn { display: inline; }
    .card.editing .answer {
      outline: 2px dashed #c9a96e !important; outline-offset: 4px;
      min-height: 40px;
    }
    .edit-btn-row {
      display: flex; gap: 6px; margin-top: 6px;
    }
    .card .edited-badge { font-size: 11px; color: #c9a96e; margin-left: 6px; }
  `;
  document.head.appendChild(style);

  const STORAGE_KEY = 'interview-edits-' + SECTION;
  let editMode = false;

  // —— 加载已保存的修改 ——
  function loadEdits() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}'); } catch (e) { return {}; }
  }
  function saveEdits(edits) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(edits));
  }

  // —— 给每个题目卡片添加编辑按钮和数据属性 ——
  function initCards() {
    document.querySelectorAll('.card').forEach((card, i) => {
      const qNum = card.querySelector('.q-num');
      if (!qNum) return;
      const qid = qNum.textContent.trim();
      card.setAttribute('data-qid', qid);

      // 恢复已保存的修改
      const edits = loadEdits();
      if (edits[qid]) {
        const answer = card.querySelector('.answer');
        if (answer) answer.innerHTML = edits[qid];
        // 加编辑标记
        const header = card.querySelector('.card-header');
        if (header && !header.querySelector('.edited-badge')) {
          const badge = document.createElement('span');
          badge.className = 'edited-badge';
          badge.title = '该题答案已被修改过';
          badge.textContent = ' ✏️';
          badge.style.cssText = 'font-size:11px;color:#c9a96e;margin-left:6px';
          header.appendChild(badge);
        }
      }

      // 编辑按钮（仅编辑模式可见）
      const btnRow = card.querySelector('.card-body');
      if (!btnRow) return;
      if (btnRow.querySelector('.edit-btn-row')) return;

      const editRow = document.createElement('div');
      editRow.className = 'edit-btn-row';
      editRow.style.cssText = 'display:none;margin-top:8px;gap:6px;';
      editRow.style.display = editMode ? 'flex' : 'none';

      const editBtn = document.createElement('button');
      editBtn.className = 'edit-answer-btn';
      editBtn.textContent = '✏️ 编辑此题';
      editBtn.style.cssText = 'font-size:11px;padding:3px 10px;border:1px solid #c9a96e;background:#faf5ed;color:#8a7a5a;border-radius:12px;cursor:pointer;transition:.2s';
      editBtn.onmouseenter = () => { editBtn.style.background = '#c9a96e'; editBtn.style.color = '#fff'; };
      editBtn.onmouseleave = () => { editBtn.style.background = '#faf5ed'; editBtn.style.color = '#8a7a5a'; };
      editBtn.onclick = () => startEdit(card, qid);

      const resetBtn = document.createElement('button');
      resetBtn.textContent = '↺ 恢复原文';
      resetBtn.style.cssText = 'font-size:11px;padding:3px 10px;border:1px solid #ccc;background:#fff;color:#999;border-radius:12px;cursor:pointer;transition:.2s';
      resetBtn.onmouseenter = () => { resetBtn.style.background = '#f5f5f5'; };
      resetBtn.onmouseleave = () => { resetBtn.style.background = '#fff'; };
      resetBtn.onclick = () => resetEdit(card, qid);

      editRow.appendChild(editBtn);
      const edits2 = loadEdits();
      if (edits2[qid]) {
        editRow.appendChild(resetBtn);
      }
      btnRow.appendChild(editRow);
    });
  }

  // —— 开始编辑 ——
  function startEdit(card, qid) {
    const answer = card.querySelector('.answer');
    if (!answer) return;

    // 如果已经在编辑中，保存
    if (answer.getAttribute('contenteditable') === 'true') {
      finishEdit(card, qid);
      return;
    }

    // 展开答案
    if (!answer.classList.contains('show')) {
      answer.classList.add('show');
      const toggleBtn = card.querySelector('.toggle-btn');
      if (toggleBtn) toggleBtn.classList.add('open');
    }

    answer.setAttribute('contenteditable', 'true');
    answer.style.outline = '2px dashed #c9a96e';
    answer.style.outlineOffset = '4px';
    answer.focus();

    // 改按钮文字
    const editBtn = card.querySelector('.edit-answer-btn');
    if (editBtn) {
      editBtn.textContent = '✔ 保存修改';
      editBtn.style.borderColor = '#2e7d32';
      editBtn.style.color = '#2e7d32';
      editBtn.onmouseenter = () => { editBtn.style.background = '#2e7d32'; editBtn.style.color = '#fff'; };
      editBtn.onmouseleave = () => { editBtn.style.background = '#e8f5e9'; editBtn.style.color = '#2e7d32'; };
      editBtn.style.background = '#e8f5e9';
    }
  }

  // —— 完成编辑 ——
  function finishEdit(card, qid) {
    const answer = card.querySelector('.answer');
    if (!answer) return;

    answer.setAttribute('contenteditable', 'false');
    answer.style.outline = 'none';
    answer.style.outlineOffset = '0';

    const newContent = answer.innerHTML.trim();
    const edits = loadEdits();
    edits[qid] = newContent;
    saveEdits(edits);

    // 添加编辑标记
    const header = card.querySelector('.card-header');
    if (header && !header.querySelector('.edited-badge')) {
      const badge = document.createElement('span');
      badge.className = 'edited-badge';
      badge.title = '该题答案已被修改过';
      badge.textContent = ' ✏️';
      badge.style.cssText = 'font-size:11px;color:#c9a96e;margin-left:6px';
      header.appendChild(badge);
    }

    // 恢复按钮
    const editBtn = card.querySelector('.edit-answer-btn');
    if (editBtn) {
      editBtn.textContent = '✏️ 编辑此题';
      editBtn.style.borderColor = '#c9a96e';
      editBtn.style.color = '#8a7a5a';
      editBtn.style.background = '#faf5ed';
      editBtn.onmouseenter = () => { editBtn.style.background = '#c9a96e'; editBtn.style.color = '#fff'; };
      editBtn.onmouseleave = () => { editBtn.style.background = '#faf5ed'; editBtn.style.color = '#8a7a5a'; };
    }

    // 显示恢复按钮
    const editRow = card.querySelector('.edit-btn-row');
    if (editRow && !editRow.querySelector('.reset-btn')) {
      const resetBtn = document.createElement('button');
      resetBtn.className = 'reset-btn';
      resetBtn.textContent = '↺ 恢复原文';
      resetBtn.style.cssText = 'font-size:11px;padding:3px 10px;border:1px solid #ccc;background:#fff;color:#999;border-radius:12px;cursor:pointer;transition:.2s';
      resetBtn.onmouseenter = () => { resetBtn.style.background = '#f5f5f5'; };
      resetBtn.onmouseleave = () => { resetBtn.style.background = '#fff'; };
      resetBtn.onclick = () => resetEdit(card, qid);
      editRow.appendChild(resetBtn);
    }
  }

  // —— 恢复原始答案 ——
  function resetEdit(card, qid) {
    const edits = loadEdits();
    delete edits[qid];
    saveEdits(edits);

    // 移除编辑标记
    const badge = card.querySelector('.edited-badge');
    if (badge) badge.remove();

    // 移除恢复按钮
    const resetBtn = card.querySelector('.reset-btn');
    if (resetBtn) resetBtn.remove();

    // 重新加载页面来恢复原始HTML
    alert('已清除该题修改，刷新页面后恢复原文。');
  }

  // —— 切换编辑模式 ——
  function toggleEditMode() {
    editMode = !editMode;
    const btn = document.getElementById('edit-mode-btn');
    if (btn) {
      btn.classList.toggle('active', editMode);
      btn.textContent = editMode ? '✏️ 退出编辑' : '✏️ 编辑模式';
    }

    document.querySelectorAll('.edit-btn-row').forEach(row => {
      row.style.display = editMode ? 'flex' : 'none';
    });

    // 退出编辑模式时，保存所有正在编辑的答案
    if (!editMode) {
      document.querySelectorAll('.answer[contenteditable="true"]').forEach(answer => {
        const card = answer.closest('.card');
        const qid = card.getAttribute('data-qid');
        if (card && qid) finishEdit(card, qid);
      });
    }

    localStorage.setItem('interview-edit-mode-' + SECTION, editMode ? '1' : '0');
  }

  // —— 导出修改 ——
  function exportEdits() {
    const edits = loadEdits();
    const keys = Object.keys(edits);
    if (keys.length === 0) {
      alert('当前板块没有修改记录。');
      return;
    }

    // 生成修改后的完整 HTML
    const clone = document.documentElement.cloneNode(true);
    clone.querySelectorAll('.card').forEach(card => {
      const qid = card.getAttribute('data-qid');
      if (edits[qid]) {
        const answer = card.querySelector('.answer');
        if (answer) answer.innerHTML = edits[qid];
      }
    });

    // 移除编辑模式相关元素
    clone.querySelectorAll('.edit-btn-row, .edited-badge, #edit-mode-btn').forEach(el => el.remove());
    clone.querySelectorAll('.answer').forEach(el => {
      el.removeAttribute('contenteditable');
      el.style.outline = 'none';
    });

    const html = '<!DOCTYPE html>\n' + clone.outerHTML;
    const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = document.title.replace(/[\\/:*?"<>|]/g, '_') + '_修改版.html';
    a.click();
    URL.revokeObjectURL(url);
  }

  // —— 页面初始化 ——
  function init() {
    initCards();

    // 恢复编辑模式状态
    editMode = localStorage.getItem('interview-edit-mode-' + SECTION) === '1';
    if (editMode) {
      document.querySelectorAll('.edit-btn-row').forEach(row => { row.style.display = 'flex'; });
    }

    // 监听 toggle 按钮，展开后显示编辑按钮
    document.querySelectorAll('.toggle-btn').forEach(btn => {
      btn.addEventListener('click', function () {
        const card = this.closest('.card');
        const editRow = card.querySelector('.edit-btn-row');
        if (editRow && editMode) {
          // 延迟一点等 answer 展开
          setTimeout(() => { editRow.style.display = 'flex'; }, 300);
        }
      });
    });
  }

  // —— 暴露到全局 ——
  window.toggleEditMode = toggleEditMode;
  window.exportEdits = exportEdits;

  // 页面加载完成后初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
