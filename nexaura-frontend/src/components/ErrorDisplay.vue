<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-red-50 text-red-700 p-4">
    <div class="text-center bg-white p-8 rounded-lg shadow-lg border border-red-200">
      <h1 class="text-3xl font-bold mb-4">糟糕，出错了</h1>
      <p class="mb-6">应用遇到一个无法恢复的错误。这很可能是由浏览器插件冲突引起的。</p>
      <div class="space-y-4 text-left bg-red-50 p-4 rounded-md">
        <p class="font-semibold">您可以尝试以下步骤来解决问题：</p>
        <ul class="list-disc list-inside">
          <li>在浏览器的无痕/隐私模式下访问本站。</li>
          <li>暂时禁用所有浏览器插件（特别是钱包类插件）后刷新页面。</li>
        </ul>
      </div>
      <button
        @click="reloadPage"
        class="mt-6 px-6 py-2 font-bold text-white bg-red-600 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
      >
        刷新页面
      </button>
    </div>
  </div>
</template>

<script setup>
const reloadPage = () => {
  window.location.reload();
};
</script> 