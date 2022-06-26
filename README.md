# C Sourcecode Cleanup Tool

Tool to diagnose and cleanup C sourcecode.

## Contents

1. Find repeated static initialization of variables.

## Limitations

1. This only works on C code. Not tested on C++.
2. The tool needs access to the C sourcecode, not binaries + headers.
3. The author(s) decline any responsibility.

## Examples

### Repeated initializations

Given this code:

```c
void declaration_1(void) {
    uint8_t counter_b[] = {0x01, 0, 0, 0};
}
uint16_t declaration_2(void) {
    uint8_t counter_a[4] = {0x01, 0x00, 0x00, 0x00};
}
```

The tool will diagnose `counter_b` and `counter_a `as the same value.

(see `test_parsing_spike_test.py`)

