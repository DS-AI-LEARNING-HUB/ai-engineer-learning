# NimbusFlow — FAQ & Troubleshooting

## Frequently Asked Questions

**Q: Can I run more than one pipeline at the same time?**
Yes. All tiers support concurrent pipeline execution; the Starter tier
caps concurrent runs at 5, Team at 25, and Enterprise is unlimited.

**Q: What happens if an action fails mid-pipeline?**
By default, the pipeline stops and the run is marked "Failed." You can
enable **retry policies** per-action in the pipeline editor to
automatically retry a failed action up to 3 times before stopping.

**Q: Does NimbusFlow store the data that passes through a pipeline?**
Only pipeline metadata (run history, timestamps, status) is stored
long-term. Payload data is held in memory during execution and discarded
after the run completes, unless you explicitly enable "Run Data Logging"
in pipeline settings.

## Common Errors

### Error: "Trigger not firing"

Usually caused by one of:
- The trigger's webhook URL was regenerated but not updated at the source
- The pipeline is paused (check the toggle in the top-right of the editor)
- Rate limiting — Starter tier triggers are capped at 100/minute

See the screenshot below for where the pause toggle lives:

![Pipeline editor showing the pause toggle location](https://example.com/images/nimbusflow-pause-toggle.png)

### Error: "Connector unreachable"

This means the on-premise connector (see the Installation Guide) has lost
its connection to NimbusFlow's control plane. Check connector logs first,
then confirm outbound HTTPS access to `*.nimbusflow.example.com` is not
being blocked by a newly-changed firewall rule.

### Error: "Action execution timeout"

Each action has a default 30-second execution timeout. For actions that
call slow external APIs, increase the timeout in the action's advanced
settings, up to a maximum of 5 minutes.

## Getting More Help

If none of the above resolves your issue, contact support with your
pipeline ID and a timestamp of the failed run.
