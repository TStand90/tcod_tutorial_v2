# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>
"""
A priority queue scheduler for use in game development.
See the queued turns time system:
http://www.roguebasin.com/index.php?title=Time_Systems#Queued_turns
"""
import heapq
from typing import Any, List, NamedTuple, Iterable, Iterator


class Ticket(NamedTuple):
    time: int
    uid: int
    value: Any


class TurnQueue(Iterable[Ticket]):
    def __init__(
        self, time: int = 0, next_uid: int = 0, heap: Iterable[Ticket] = (),
    ) -> None:
        self.time = time  # Current time.
        self.next_uid = next_uid  # Sorting tie-breaker.
        # Priority queue of events maintained by heapq
        self.heap: List[Ticket] = list(heap)
        heapq.heapify(self.heap)

    def schedule(self, interval: int, value: Any) -> Ticket:
        """Schedule and return a new ticket for `value` after `interval` time.
        `interval` must be an integer, or else precision will be permanently
        lost.
        """
        ticket = Ticket(self.time + interval, self.next_uid, value)
        heapq.heappush(self.heap, ticket)
        self.next_uid += 1  # Sort tickets with the same time in FIFO order.
        return ticket

    def next(self) -> Ticket:
        """Pop and return the next scheduled ticket."""
        ticket = heapq.heappop(self.heap)
        self.time = ticket.time
        return ticket

    def __iter__(self) -> Iterator[Ticket]:
        """Return an iterator that exhausts the tickets in the queue.
        New tickets can be scheduled during iteration.
        """
        while self.heap:
            yield self.next()

    def __repr__(self) -> str:
        """A string representation of this instance, including all tickets."""
        return "%s(time=%r, next_uid=%r, heap=%r)" % (
            self.__class__.__name__,
            self.time,
            self.next_uid,
            self.heap,
        )


__all__ = (
    "Ticket",
    "TurnQueue",
)
