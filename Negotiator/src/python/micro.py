import random

from negmas.outcomes import Outcome
from negmas.preferences import PresortingInverseUtilityFunction
from negmas.sao import ResponseType, SAONegotiator, SAOResponse, SAOState
from typing import Union  
__all__ = ["MiCRO"]


class MiCRO(SAONegotiator):
    """
    A simple implementation of the MiCRO negotiation strategy

    Remarks:
        - This is a simplified implementation of the MiCRO strategy.
        - It is not guaranteed to exactly match the published work.
        - MiCRO was introduced here:
          de Jonge, Dave. "An Analysis of the Linear Bilateral ANAC Domains Using the MiCRO Benchmark Strategy."
          Proceedings of the Thirty-First International Joint Conference on Artificial Intelligence, IJCAI. 2022.
        - Note that MiCRO works optimally if both negotiators can concede all the way to agreement. If one of them
          has a high reservation value preventing it from doing so, or if the allowed number of steps is small, MiCRO
          will not reach agreement (even against itself).请注意，如果谈判者双方都能让步达成一致，那么微谈判的效果是最佳的。
          如果其中一个保留值很高，阻止它这样做，或者如果允许的步骤数很小，MiCRO将无法达成协议(甚至反对自己)。
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # initialize local variables
        self.worst_offer_utility: float = float("inf")
        self.sorter = None
        self._received, self._sent = set(), set()

    def __call__(self, state: SAOState) -> SAOResponse:
        # The main implementation of the MiCRO strategy
        assert self.ufun
        # initialize the sorter (This should better be done in on_negotiation_start() to allow for reuse but this is not needed in ANL)
        if self.sorter is None:
            # A sorter, sorts a ufun and can be used to get outcomes using their utiility
            #一个排序器，排序一个unfun，可以用来获得结果使用他们的效用 
            self.sorter = PresortingInverseUtilityFunction(
                self.ufun, rational_only=True, eps=-1, rel_eps=-1
            )
            # Initialize the sorter. This is an O(nlog n) operation where n is the number of outcomes
            # #初始化排序器这是一个O(nlog n)的操作，其中n是结果的个数
            self.sorter.init()
        # get the current offer and prepare for rejecting it
        # get目前的报价，并准备拒绝它
        offer = state.current_offer

        # If I received something, check for acceptance
        if offer is not None:
            self._received.add(offer)

        # Find out my next offer and the acceptable offer
        will_concede = len(self._sent) <= len(self._received)
        # My next offer is either a conceding outcome if will_concede or sampled randomly from my past offers
        # 我的下一个报价要么是让步的结果，要么是从我过去的报价中随机抽取的
        next_offer = (
            self.sample_sent() if not will_concede else self.sorter.next_worse()
        )
        # If I exhausted all my rational offers, do not concede
        if next_offer is None:
            will_concede, next_offer = False, self.sample_sent()
        else:
            next_utility = float(self.ufun(next_offer))
            if next_utility < self.ufun.reserved_value:
                will_concede, next_offer = False, self.sample_sent()
        next_utility = float(self.ufun(next_offer))
        # Find my acceptable outcome. It will None if I did not offer anything yet.
        acceptable_utility = (
            self.worst_offer_utility if not will_concede else next_utility
        )

        # The Acceptance Policy of MiCRO
        # accept if the offer is not worse than my acceptable offer if I am conceding or the best so far if I am not
        # MiCRO的接受政策
        # 如果我做出让步，那么这个报价就不会比我的可接受报价差，如果我不让步，那么这个报价就会是目前为止最好的
        offer_utility = float(self.ufun(offer))
        if (
            offer is not None
            and offer_utility >= acceptable_utility
            and offer_utility >= self.ufun.reserved_value
        ):
            return SAOResponse(ResponseType.ACCEPT_OFFER, offer)
        # If I cannot find any offers, I know that there are NO rational outcomes in this negotiation for me and will end it.
        # 如果我找不到任何报价，我知道这次谈判对我来说没有合理的结果，我会结束它。
        if next_offer is None:
            return SAOResponse(ResponseType.END_NEGOTIATION, None)
        # Offer my next-offer and record it
        self._sent.add(next_offer)
        self.worst_offer_utility = next_utility
        return SAOResponse(ResponseType.REJECT_OFFER, next_offer)

    def sample_sent(self) -> Union[Outcome, None]:
        # Get an outcome from the set I sent so far (or my best if I sent nothing)
        # 从我迄今为止发送的集合中获取结果(如果我没有发送，则获取我最好的结果)
        if not len(self._sent):
            return None
        return random.choice(list(self._sent))
