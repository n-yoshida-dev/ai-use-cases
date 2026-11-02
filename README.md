# AI Use Cases

ChatGPT・Claude.aiのチャット／Work／スケジュール（Claude Codeのルーティンを含む）で、AIへ任せる作業と人間の判断を設計した事例集。図から概要をつかみ、気になるケースへ進めます。

## 仕組み全体

| 日々のタスク管理 | 文脈と読書の循環 | 横断タスクボード |
| --- | --- | --- |
| [![Todoistへ集まる入力と毎日の整理](systems/daily-task-hub/cover.png)](systems/daily-task-hub/) | [![複数AI・コンテキスト・読書の連携](systems/context-reading-loop/cover.png)](systems/context-reading-loop/) | [![タスク・予定・リポジトリの作業を1枚のボードへ](systems/cross-task-board/cover.png)](systems/cross-task-board/) |
| **[メール・音声・手入力から実行へ](systems/daily-task-hub/)** | **[会話の文脈から次に読む本へ](systems/context-reading-loop/)** | **[今日やることを1枚のボードに](systems/cross-task-board/)** |

[全体構成の一覧](systems/README.md)

## 個別ケース

| GUI作業の委譲 | 定期レビューの自動化 | 毎朝のメール仕分け |
| --- | --- | --- |
| [![YouTube整理の仕組み](cases/youtube-playlist-cleanup/cover.png)](cases/youtube-playlist-cleanup/) | [![定期レビューの仕組み](cases/scheduled-reviews/cover.png)](cases/scheduled-reviews/) | [![メール仕分けの仕組み](cases/daily-email-triage/cover.png)](cases/daily-email-triage/) |
| **[YouTubeマイリスト整理](cases/youtube-playlist-cleanup/)** | **[スケジュールによる定期レビュー](cases/scheduled-reviews/)** | **[毎朝のメール仕分け](cases/daily-email-triage/)** |
| AIが棚卸し・分類・操作を担当。人間が整理方針を決める。 | AIが定期的に情報を確認・分析。人間が方針と次の行動を決める。 | AIが毎朝読んで仕分け・通知。人間が判定基準を決め、対応する。 |
| 本人申告で整理完了／件数・変更前後は未確認 | 現行設定・直近の完了記録と保存報告を確認／成果物の独立検証・効果測定は未実施 | 設定・出力を確認／判定の正確さと効果は未測定 |

| 毎朝のタスク整理 | ブックマークの整理 | 買い物の計画 |
| --- | --- | --- |
| [![Todoist整理の仕組み](cases/daily-todoist-triage/cover.png)](cases/daily-todoist-triage/) | [![保存から活用への仕組み](cases/bookmark-to-action/cover.png)](cases/bookmark-to-action/) | [![買い物計画の仕組み](cases/allowance-shopping-plan/cover.png)](cases/allowance-shopping-plan/) |
| **[毎朝のTodoist整理](cases/daily-todoist-triage/)** | **[ブックマークを使える情報へ](cases/bookmark-to-action/)** | **[お小遣いの買い物計画](cases/allowance-shopping-plan/)** |
| AIがInboxの分類・期限・順序を整理。人間が優先度と除外範囲を決める。 | AIが分類・移行。人間が保存先・例外・使う情報を決める。 | AIが欲しいものを読み、積立を分けた計画を画面に。人間が入力と順番を決める。 |
| 現行設定・直近の完了記録と更新検証の報告を確認／結果の独立検証・効果測定は未実施 | 初回整理を確認／定期は停止中・気づいたときに依頼 | 試作・改善中。初回の画面を確認／効果は未測定 |

| 横断のスケジュール | 商品比較の記録 | 記事の執筆と投稿 |
| --- | --- | --- |
| [![横断タスクボードで1日を組む仕組み](cases/daily-cross-task-board/cover.png)](cases/daily-cross-task-board/) | [![会話から商品メモと購入判断ノートを整理する仕組み](cases/shopping-decision-notes/cover.png)](cases/shopping-decision-notes/) | [![聞き取りから記事を書いて投稿する仕組み](cases/article-drafting-workflow/cover.png)](cases/article-drafting-workflow/) |
| **[横断タスクボードで今日と明日を組む](cases/daily-cross-task-board/)** | **[商品比較の判断をNotionに残す](cases/shopping-decision-notes/)** | **[聞き取りから記事を書き、投稿まで](cases/article-drafting-workflow/)** |
| AIがタスク・予定・各リポジトリを読み、時刻と配分の予定をボードに。人間が型を決め、見て実行する。 | AIが比較の経緯を整理。人間が判断基準を伝え、解釈を訂正する。 | AIが資料を読んで質問し、下書き・校正・限定共有の投稿。人間が声で答え、直し、公開する。 |
| 8日分の作業記録で更新と検算を確認／効果は未測定 | 判断ノートの保存内容と導線を確認／記事での再利用・継続効果は未検証 | Qiitaの記事1本の公開と書き直しを確認／noteの自動下書き・効果は未検証 |

| 次の会話への作業メモ | 開発の観測画面 |
| --- | --- |
| [![作業を終える前に作業メモと本人待ちをファイルに書き、次の会話が読んで続ける仕組み](cases/handoff-and-todo-files/cover.png)](cases/handoff-and-todo-files/) | [![開発の状態を1画面に集める、常に動くプログラム](cases/dev-dashboard-hub/cover.png)](cases/dev-dashboard-hub/) |
| **[次の会話への作業メモと、本人待ちの置き場](cases/handoff-and-todo-files/)** | **[開発の状態を1画面に集めて常駐させる](cases/dev-dashboard-hub/)** |
| AIが作業を終える前に次の会話への作業メモと本人待ちを書き、答えを記録。人間が会話で答える。 | AIが正本を読んで描く画面を各リポジトリに作る。人間が足す先と指標を決め、見るだけ。 |
| 決まり・点検スクリプト・フック・TODO.mdへ移したコミットを確認／古くならずに続くか・効果は未検証 | 常駐と4リポジトリが1画面に並ぶことを確認／見る頻度と効果は未測定 |

図は仕組みの概念図です。実画面や実績の証拠ではありません。
図のサービスのロゴは各社の商標で、サービスを指すためにだけ使っています（出どころは [scripts/logos/README.md](scripts/logos/README.md)）。

Claude Code製の独立アプリ・プロジェクトは、各リポジトリとポートフォリオで紹介します。

<details>
<summary>AIでケースを追加・更新する方へ（最初に読む）</summary>

**最初に最新mainの [AGENTS.md](AGENTS.md) を全文読み、指定された読み取り順に従ってください。** 操作方法やチャットが変わっても、このファイルが方針の正本です。

別チャットでは次の開始文を使えます。

```text
GitHubの n-yoshida-dev/ai-use-cases を対象に、今回のAI活用事例を記録してください。
最初に最新mainのAGENTS.mdを全文読み、そこに指定された順でREADME・記録プロンプト・テンプレート・関連ケースを読んでください。
登録対象・日本語の概念図・公開ルールを守り、同じ事例があれば更新してください。
参照できない会話や未確認の成果を補わないでください。
```

[記録プロンプト](prompts/capture-case.md) ／ [図の仕様](templates/cover-brief.md)

指示ファイルは別チャットへ自動配信されません。依頼時にリポジトリと読み取り指定を渡してください。

</details>
