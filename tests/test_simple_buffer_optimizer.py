import sys, os, pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ssd_core.optimizer.simple_buffer_optimizer import SimpleBufferOptimizer
from validator import Packet

test_cases = test_cases_pretty = [

    # 1. 중복 Write 제거
    (
        [
            Packet("W", 10, 0x11111111),  # 제거됨
            Packet("W", 10, 0x22222222),  # 유지
        ],
        [
            Packet("W", 10, 0x22222222),  # 최종 결과
        ]
    ),

    # 2. 여러 중복 Write 제거
    (
        [
            Packet("W", 5, 0x11111111),  # 제거됨
            Packet("W", 5, 0x22222222),  # 제거됨
            Packet("W", 5, 0x33333333),  # 유지
        ],
        [
            Packet("W", 5, 0x33333333),  # 최종 결과
        ]
    ),

    # 3. Erase가 Write 무효화
    (
        [
            Packet("W", 20, 0xABCD1234),  # 제거됨
            Packet("E", 19, 2),  # 유지
        ],
        [
            Packet("E", 19, 2),  # 최종 결과
        ]
    ),

    # 4. Erase가 Write에 영향 없음
    (
        [
            Packet("W", 20, 0xABCD1234),  # 유지
            Packet("E", 10, 5),  # 유지
        ],
        [
            Packet("E", 10, 5),
            Packet("W", 20, 0xABCD1234),  # 최종 결과
        ]
    ),

    # 5. Erase 병합 (연속 영역)
    (
        [
            Packet("E", 30, 5),  # 병합됨
            Packet("E", 35, 3),  # 병합됨
        ],
        [
            Packet("E", 30, 8),  # 최종 결과
        ]
    ),

    # 6. Erase 병합 불가 (간격 존재)
    (
        [
            Packet("E", 30, 3),  # 유지
            Packet("E", 40, 2),  # 유지
        ],
        [
            Packet("E", 30, 3),  # 최종 결과
            Packet("E", 40, 2),
        ]
    ),

    # 7. 병합은 가능하나 size > 10 → 병합하지 않음
    (
        [
            Packet("E", 10, 6),  # 유지
            Packet("E", 16, 6),  # 유지
        ],
        [
            Packet("E", 10, 6),  # 최종 결과
            Packet("E", 16, 6),
        ]
    ),

    # 8. 중복 W 제거 + Erase로 W 제거 + Erase 병합
    (
        [
            Packet("W", 1, 0x11111111),  # 제거됨
            Packet("W", 1, 0x22222222),  # 제거됨 (erase로 무효화)
            Packet("E", 0, 2),  # 병합됨
            Packet("E", 2, 2),  # 병합됨
        ],
        [
            Packet("E", 0, 4),  # 최종 결과
        ]
    ),

    # 9. Write가 Erase 범위 밖 → 유지
    (
        [
            Packet("E", 90, 5),  # 유지
            Packet("W", 80, 0xABCD1234),  # 유지
        ],
        [
            Packet("E", 90, 5),  # 최종 결과
            Packet("W", 80, 0xABCD1234),
        ]
    ),

    # 10. 모든 Write 무효화됨
    (
        [
            Packet("W", 1, 0x11111111),  # 제거됨
            Packet("W", 1, 0x22222222),  # 제거됨
            Packet("E", 0, 5),
        ],
        [
            Packet("E", 0, 5),  # 최종 결과
        ]
    ),

    # 11. 중복 Erase
    (
        [
            Packet("E", 0, 5),  # 제거됨
            Packet("E", 0, 5),  # 유지
        ],
        [
            Packet("E", 0, 5),  # 최종 결과
        ]
    ),

    # 12. Erase가 포함되는 경우 유지
    (
        [
            Packet("E", 10, 5),  # 유지
            Packet("E", 10, 2),  # 제거됨
        ],
        [
            Packet("E", 10, 5),  # 최종 결과
        ]
    ),

    # 13. 연속 병합 (총 10 이하)
    (
        [
            Packet("E", 0, 5),  # 병합됨
            Packet("E", 5, 5),  # 병합됨
        ],
        [
            Packet("E", 0, 10),  # 최종 결과
        ]
    ),

    # 14. 중첩 유지
    (
        [
            Packet("E", 10, 5),  # 제거됨
            Packet("E", 10, 7),  # 유지
        ],
        [
            Packet("E", 10, 7),  # 최종 결과
        ]
    ),

    # 15. 병합 가능한 중첩 + 뒤는 포함
    (
        [
            Packet("E", 10, 5),  # 제거됨
            Packet("E", 10, 7),  # 병합됨
            Packet("E", 12, 3),  # 제거됨 (포함)
        ],
        [
            Packet("E", 10, 7),  # 최종 결과
        ]
    ),

    # 16. 병합 후 slicing (20칸 → 10+10)
    (
        [
            Packet("E", 0, 7),  # 병합
            Packet("E", 7, 7),  # 병합
            Packet("E", 14, 6),  # 병합
        ],
        [
            Packet("E", 0, 10),  # 최종 결과
            Packet("E", 10, 10),
        ]
    ),

    # 17. 뒤 Erase로 앞 Write 무효화
    (
        [
            Packet("W", 1, 0xABCD1234),  # 제거됨
            Packet("W", 3, 0xABCD1234),  # 제거됨
            Packet("W", 5, 0xABCD1234),  # 제거됨
            Packet("E", 0, 10),  # 유지
        ],
        [
            Packet("E", 0, 10),  # 최종 결과
        ]
    ),

    # 18. 앞 Erase → 뒤 Write는 무효 안됨
    (
        [
            Packet("E", 0, 10),  # 유지
            Packet("W", 1, 0xABCD1234),  # 유지
            Packet("W", 3, 0xABCD1234),  # 유지
            Packet("W", 5, 0xABCD1234),  # 유지
        ],
        [
            Packet("E", 0, 10),  # 최종 결과
            Packet("W", 1, 0xABCD1234),
            Packet("W", 3, 0xABCD1234),
            Packet("W", 5, 0xABCD1234),
        ]
    ),

    # 19. write로 덮는 영역이 erase들을 잇는 경우
    (
        [
            Packet("E", 0, 2),  # 병합
            Packet("E", 3, 2),  # 병합
            Packet("E", 6, 2),  # 병합
            Packet("W", 2, 0xABCD1234),  # 유지
            Packet("W", 5, 0xABCD1234),  # 유지
        ],
        [
            Packet("E", 0, 8),  # 최종 결과
            Packet("W", 2, 0xABCD1234),
            Packet("W", 5, 0xABCD1234),
        ]
    ),

    # 20. 빈 버퍼 → 빈 결과
    (
        [
            # 빈
        ],
        [
            # 빈
        ]
    ),

    # 21. 단일 Write → 그대로 유지
    (
        [
            Packet("W", 42, 0xABCD1234),  # 유지
        ],
        [
            Packet("W", 42, 0xABCD1234),  # 최종 결과
        ]
    ),

    # 22. 단일 Erase → 그대로 유지
    (
        [
            Packet("E", 5, 10),  # 유지
        ],
        [
            Packet("E", 5, 10),  # 최종 결과
        ]
    ),

    # 23. 연속 Erase 2개(합쳐서 ≤10) → 병합
    (
        [
            Packet("E", 0, 4),  # 병합됨
            Packet("E", 4, 5),  # 병합됨
        ],
        [
            Packet("E", 0, 9),  # 최종 결과
        ]
    ),

    # 24. write bridge로 연결 가능한 write 영역 2개와 erase 최대 길이 초과로 연결 불가능한 erase 1개 조합
    # return case가 여러 가지 일 수 있음
    ([Packet("E", 0, 4),
      Packet("W", 4, 0x4),
      Packet("W", 10, 0x10),
      Packet("E", 5, 5),
      Packet("E", 11, 3)],
     [Packet("E", 0, 10),
      Packet("E", 10, 4),
      Packet("W", 4, 0x4),
      Packet("W", 10, 0x10)]),

]


@pytest.mark.parametrize("buf_in, expected", test_cases, ids=[f"case_{i + 1}" for i in range(len(test_cases))])
def test_buffer_optimizer(buf_in, expected):
    optimizer = SimpleBufferOptimizer()
    result = optimizer.calculate(buf_in)

    try:
        assert len(result) == len(expected), (
            f"\n❌ Length mismatch:\n"
            f"Input:    {buf_in}\n"
            f"Expected: {expected}\n"
            f"Got:      {result}\n"
        )

        for i, (r, e) in enumerate(zip(result, expected)):
            assert r.COMMAND == e.COMMAND, (
                f"\n❌ COMMAND mismatch at index {i}:\n"
                f"Input:    {buf_in}\n"
                f"Expected: {expected}\n"
                f"Got:      {result}\n"
            )
            assert r.ADDR == e.ADDR, (
                f"\n❌ ADDR mismatch at index {i}:\n"
                f"Input:    {buf_in}\n"
                f"Expected: {expected}\n"
                f"Got:      {result}\n"
            )
            assert r.VALUE == e.VALUE, (
                f"\n❌ VALUE mismatch at index {i}:\n"
                f"Input:    {buf_in}\n"
                f"Expected: {expected}\n"
                f"Got:      {result}\n"
            )

    except AssertionError as e:
        print(str(e))
        raise
