ifeq ($(SCHED_DIR),)
  SCHED_DIR = scheduler
endif

CFILES +=  $(wildcard $(SCHED_DIR)/*.c)
INCDIR += $(SCHED_DIR)  