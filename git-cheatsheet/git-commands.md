# Git 常用操作指令速查表

> 一份日常开发中最常用的 Git 命令清单，按使用场景分类整理，方便随时查阅。

## 目录
- [一、仓库初始化与配置](#一仓库初始化与配置)
- [二、基础工作流（增删改提交）](#二基础工作流增删改提交)
- [三、分支管理](#三分支管理)
- [四、远程仓库协作](#四远程仓库协作)
- [五、查看与对比](#五查看与对比)
- [六、撤销与回退](#六撤销与回退)
- [七、暂存与补丁](#七暂存与补丁)
- [八、标签管理](#八标签管理)
- [九、进阶与实用技巧](#九进阶与实用技巧)

---

## 一、仓库初始化与配置

```bash
# 在当前目录初始化新仓库
git init

# 克隆远程仓库到本地
git clone <仓库地址>
git clone <仓库地址> <本地目录名>     # 指定目录名

# 查看全局配置
git config --global --list

# 设置用户名和邮箱（提交会用到）
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"

# 设置默认分支名为 main
git config --global init.defaultBranch main

# 查看当前仓库状态
git status
```

---

## 二、基础工作流（增删改提交）

```bash
# 把文件加入暂存区
git add <文件名>
git add .                       # 添加所有改动（含新增、修改）
git add -A                      # 添加所有改动（含删除）
git add -p                      # 交互式地按区块添加

# 提交到本地仓库
git commit -m "提交说明"
git commit -am "提交说明"        # 自动暂存已跟踪文件的修改并提交（不含新文件）
git commit --amend              # 修改上一次提交（补充内容或改说明）

# 查看提交历史
git log
git log --oneline               # 单行精简显示
git log --graph --oneline --all # 图形化显示分支
git log -n 5                    # 只看最近 5 条
```

---

## 三、分支管理

```bash
# 查看分支
git branch                      # 本地分支
git branch -a                   # 本地 + 远程分支

# 创建分支
git branch <分支名>

# 切换分支
git checkout <分支名>
git switch <分支名>             # 新版推荐方式

# 创建并切换分支
git checkout -b <分支名>
git switch -c <分支名>          # 新版推荐方式

# 删除分支
git branch -d <分支名>          # 已合并才允许删除
git branch -D <分支名>          # 强制删除

# 合并分支（在当前分支合并目标分支）
git merge <分支名>
git merge --no-ff <分支名>      # 保留合并记录（禁用快进）

# 变基（让提交历史更线性）
git rebase <分支名>
git rebase -i <commit>          # 交互式变基（整理提交）
```

---

## 四、远程仓库协作

```bash
# 查看远程仓库
git remote -v

# 添加远程仓库
git remote add origin <仓库地址>

# 拉取远程更新
git fetch                       # 仅下载，不合并
git pull                        # 下载并合并（= fetch + merge）
git pull --rebase               # 用变基方式拉取

# 推送到远程
git push                        # 推送当前分支
git push -u origin <分支名>     # 首次推送并关联上游
git push origin --delete <分支名>  # 删除远程分支

# 同步（多人协作推荐流程）
git fetch origin
git rebase origin/main          # 在本地分支变基到最新
git push
```

---

## 五、查看与对比

```bash
# 查看工作区与暂存区的差异
git diff
git diff --staged               # 暂存区与最新提交的差异
git diff <分支A> <分支B>         # 两个分支的差异

# 查看某次提交改动
git show <commit>

# 查看文件每行是谁改的（ blame ）
git blame <文件名>

# 搜索提交历史中的关键字
git log -S "关键字" --oneline
```

---

## 六、撤销与回退

```bash
# 撤销工作区修改（回到最近一次提交状态，危险！）
git checkout -- <文件名>
git restore <文件名>            # 新版推荐方式

# 把文件从暂存区撤回（保留工作区修改）
git reset HEAD <文件名>
git restore --staged <文件名>   # 新版推荐方式

# 回退到某次提交
git reset --soft <commit>       # 只回退提交，保留改动在暂存区
git reset --mixed <commit>      # 回退提交和暂存，保留工作区（默认）
git reset --hard <commit>       # 彻底回退，丢弃所有改动（危险！）

# 生成一个反向提交来抵消某次提交（推荐用于已推送的提交）
git revert <commit>
```

---

## 七、暂存与补丁

```bash
# 把当前未提交的改动暂存起来
git stash
git stash list                 # 查看暂存列表
git stash pop                  # 恢复最近一次暂存并删除
git stash apply                # 恢复但不删除
git stash drop                 # 删除最近一次暂存
git stash clear                # 清空所有暂存
```

---

## 八、标签管理

```bash
# 查看标签
git tag

# 创建标签
git tag <标签名>                # 轻量标签
git tag -a v1.0 -m "版本说明"   # 带注释标签

# 推送标签到远程
git push origin <标签名>
git push origin --tags         # 推送所有标签

# 删除标签
git tag -d <标签名>
git push origin --delete <标签名>
```

---

## 九、进阶与实用技巧

```bash
# 清理本地已删除的远程分支引用
git fetch -p

# 修改最近一次提交的作者信息
git commit --amend --author="名字 <邮箱>"

# 把多个提交压成一个（交互式变基）
git rebase -i HEAD~3           # 把最近 3 次提交整理

# 二分法定位引入 bug 的提交
git bisect start
git bisect bad                 # 当前是坏版本
git bisect good <commit>       # 指定一个好版本
# 测试后标记：git bisect good / git bisect bad
git bisect reset               # 结束二分

# 忽略文件已跟踪后想停止跟踪（仍在磁盘）
git rm --cached <文件名>

# 查看某命令帮助
git help <命令>
git <命令> --help
```

---

## 常用别名（可选配置）

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.lg "log --graph --oneline --all"
```

配置后可用 `git st`、`git cm` 等简化输入。

---

> 提示：`reset --hard`、`checkout -- <文件>` 等操作会丢弃未保存的改动，执行前请确认。已推送到远程的提交尽量用 `revert` 而非 `reset` 来撤销，避免影响协作他人。
