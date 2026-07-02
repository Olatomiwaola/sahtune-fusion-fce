# Rule: <RULE-ID> — <short name>
# Trace: <FCE-REQ-...>  Bundle: <bundle@version>  Default: deny

package fce.policy.<area>

default allow := false

# Rego-style example (reference pattern only)
allow if {
    input.object.classification in data.permits[input.mission].classifications
    input.object.domain == input.channel.domain
    valid_caveats(input.object.release_caveat, input.channel)
    not stale(input.object.timestamp)
}

# Unit-test description (no implementation yet):
# TST-POL-XXX: given <object attrs> and <channel attrs>, expect <disposition>,
# audit event with rule ID <RULE-ID>, reason code <RC>.
