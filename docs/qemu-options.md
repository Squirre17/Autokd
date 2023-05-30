- panic=-1：不进行自动重启，直接停止系统。
- panic=1：进行自动重启，默认值。

在 Linux 内核引导过程中，quiet 参数用于控制内核消息的输出。如果设置了 quiet 参数，内核会尽量减少不必要的输出信息，只输出关键信息。
- 禁止内核启动时输出详细的硬件信息。
- 禁止内核输出一些调试信息和警告信息。
- 只输出重要的错误信息。