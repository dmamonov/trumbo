# trumbo

_A Sreenwriter's Tool_

This is [LPB25](https://www.kxsb.org/lpb25) hackathon project.

> The priority of this project is to avoid script content generation at all costs.

## The Goal

To give screenwriters and film directors a productivity tool
that optimizes routine operations and reduces communication overhead —
similar to what modern [IDE](https://www.jetbrains.com/idea/) and [GitHub](https://github.com/) tools do for software
development.

## Demo

[![Watch the demo videp](assets/demo-cover.jpg)](https://www.youtube.com/watch?v=rBilzrJir-M)

## Key Ideas

A movie script is a well-structured text that:

1) have to comply with de-facto standards (e.g. Hollywood standard)
2) is used as a single source of truth to organise pre-production works (e.g. casting)

With a power of AI (LLM) a lot of routine operations with text can be done automatically.
Especially this requires a full script text analysis or cross-checking (e.g. give me a list of film characters).

Lots of pre-production works:

![script-dimensions.png](assets/script-dimensions.png)

are directly based on a script, and their content and communication can be streamlined
by providing an accurate perspective (slice) of a script with an emphasis on e certain aspect.

This, of course, works in depth:
![pre-production-dependencies.png](assets/pre-production-dependencies.png)

And potentially can be arranged with a support of a bidirectional feedback:
![script-feedback-and-iterations.png](assets/script-feedback-and-iterations.png)

where:

1) changes made in a draft-# version of a script will automatically propagate (by email or push notification) to people
   working on derivatives (e.g. costumes)
2) if some ideas appear on later stage (
   e.g. [costume](https://en.wikipedia.org/wiki/Predator_(fictional_species)#:~:text=The%20Predator%20was%20originally%20designed,weeks%2C%20ending%20in%20February%201987.))
   it shall be possible to navigate back to the script and consistently incorporate it

## Target Audience and Profitability Considerations

This tool aims as a primary collaboration platform for all cust and crew members,
not limited to a persona of a screenwriter. That is a lot of people, with a paid subscription per seat.

Subscription might be free for screenwriters themselves, to attract them into the product.

In addition, the tool can also be used in game development, which is an additional market.

## Scope of Work & Guidance

This section covers approximate plan for the duration of the hackathon (20 days, till Apr, 25).

Sure, there is no strict bounds and order of work can be mixed as you like.

Also, many steps are optional and can be omitted (if we don't have time/competence to perform them properly).

### Week-1: Research (6-13 Apr)

- [ ] Learn about screenwriting (see [Resources to Check](#resources-to-check) section)
- [ ] Check existing tools on the market
- [ ] Brainstorm ideas about potential functionality: (N)FRs
- [ ] initial draft outline of presentation video
- [ ] initial draft about High Level Design: architecture diagram, components
- [ ] more to be added...

### Week-2: Build (14-22, NB: Easter)

- [ ] draw a few high fidelity mockups to show an idea of potential app
- [ ] implement different ideas as stand-alone python-notebooks/script to prove we can solve them
- [ ] implement a small UI application with a piece of functionality (to highlight interactivity)
- [ ] initial QA/evaluation
- [ ] Create a slide deck to present the idea
- [ ] Create a pitch script
- [ ] Record a 3-5 minutes presentation video

## Guidance on Tech/Repo/Process

While it will be really great to have a resulting code integrated together
into single interactive application, that is really hard to achieve and probably
not necessary for the scope of the hackathon.

This is why the aim is to implement different pieces of functionality
separately and combine them together in the final demo-video.

It will be great to have an interactive part as an application,
but not everything have to be there.

- Feel free do to your part of the project in your own repository (if you like)
- Feel free to use any language for the project (of your choice)
- Feel free to use any technology (if you need)
- Feel free to use any IDE/Tool for work (you prefer)

P.S. `python3` is totally fine.

## Resources to Check

- [Trumbo film](https://en.wikipedia.org/wiki/Trumbo_(2015_film)) - watch the movie if you are curious about the project
  name
- [The Tools of Screenwriting book](https://www.amazon.co.uk/gp/product/0312119089) - **essential read** to grasp an
  idea of a screen/script writing. About 100 pages.
- [sudowrite app](https://sudowrite.com/) - a competing product for book writers. Please check optionally.

