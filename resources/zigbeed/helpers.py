# This file is part of Jeedom.
#
# Jeedom is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Jeedom is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Jeedom. If not, see <http://www.gnu.org/licenses/>.
import logging
import functools

def retryable_req(delays=(1, 5, 10, 15, 30, 60, 120, 180, 360, 600, 900, 1800), raise_=False):
	"""Make a method with ZCL requests retryable.This adds delays keyword argument to function.len(delays) is number of tries.raise_ if the final attempt should raise the exception.
	"""

	def decorator(func):
		@functools.wraps(func)
		async def wrapper(channel, *args, **kwargs):
			exceptions = (zigpy.exceptions.ZigbeeException, asyncio.TimeoutError)
			try_count, errors = 1, []
			for delay in itertools.chain(delays, [None]):
				try:
					return await func(channel, *args, **kwargs)
				except exceptions as ex:
					errors.append(ex)
					if delay:
						delay = uniform(delay * 0.75, delay * 1.25)
						channel.debug(("%s: retryable request #%d failed: %s. ""Retrying in %ss"),func.__name__,try_count,ex,round(delay, 1),)
						try_count += 1
						await asyncio.sleep(delay)
					else:
						channel.warning("%s: all attempts have failed: %s", func.__name__, errors)
						if raise_:
							raise
		return wrapper
	return decorator
